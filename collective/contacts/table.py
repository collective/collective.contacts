# -*- coding: utf-8 -*-

from zope.i18n import translate
from zope.interface import implements
from zope.component import getAdapter, getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import Image

from collective.contacts.interfaces import ITable, ICustomizableColumns, ISearch, IOrganization

class AbstractTable(object):
    """ Abstract table class
    
        Subclasses need to provide the following attributes:
        
        * default_sort: the default sorting (tuple of
                        field, order pairs)
        * name: the name of the corresponding CustomizableColumns
                adapter
        * attrs: list of attributes which may be searched for
        
        Additionally the following methods have to be implemented:
        
        * newSearch: returns whether a new search was issued or not
        * email: see interfaces.ITable
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cols = getAdapter(self.context, interface=ICustomizableColumns, name=self.name)
        sort = self.request.get('sort_on', None)
        sort_by = self.request.get('sort_by', 'asc')
        self.sort = tuple([(on, sort_by == 'desc' and (by == 'asc' and 'desc' or 'asc') or by) for on, by in self.default_sort if not on == sort])
        if sort is not None:
            self.sort = ((sort, sort_by),) + self.sort
            
    def reset(self):
        if not hasattr(self.request, 'SESSION'):
            return
        for attr in self.attrs:
            if self.request.SESSION.has_key('%s.%s' % (self.name, attr)):
                del self.request.SESSION['%s.%s' % (self.name, attr)]
        
    def columns(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        indexes = catalog.indexes()
        base = self.request.get('URL')
        columns = []
        for column in self.cols.get_columns():
            html = translate(self.cols.translate_column(column), context=self.request)
            sortable = 'sortable_%s' % column
            if column in indexes or sortable in indexes:
                index = sortable in indexes and sortable or column
                current = dict(self.sort[:1]).get(index, None)
                if current is not None:
                    html += current == 'asc' and ' <span class="arrowUpAlternative">&#9650;</span>' or ' <span class="arrowDownAlternative">&#9660;</span>'
                html = '<a href="%s?sort_on=%s&sort_by=%s">%s</a>' % (base, index, current == 'asc' and 'desc' or 'asc', html)
            columns.append(html)
        return columns
    
    def rows(self):
        attrs = {}
        if hasattr(self.request, 'SESSION'):
            if self.newSearch():
                attrs = {}
                for attr in self.attrs:
                    self.request.SESSION.set('%s.%s' % (self.name, attr), self.request.get('form.%s' % attr, None))
                    
            for attr in self.attrs:
                attrs[attr] = self.request.SESSION.get('%s.%s' % (self.name, attr), None)
        
        search = getAdapter(self.context, interface=ISearch, name=self.name)
        results = search.search(query=attrs, sort=self.sort)
        if not results:
            return []
    
        columns = self.cols.get_columns()
        countries = getUtility(IVocabularyFactory, name='contacts.countries')(self.context)
        states = getUtility(IVocabularyFactory, name='contacts.states')(self.context)
        rows = []
        for result in results:
            row = []
            for col in columns:
                html = '<span>'
                if col == 'country':
                    try:
                        value = countries.getTerm(result.country).title
                        if value:
                            html += value
                    except LookupError:
                        pass
                elif col == 'state':
                    try:
                        value = states.getTerm(result.state).title
                        if value:
                            html += value
                    except LookupError:
                        pass
                elif col == 'organization':
                    value = getattr(result, col, '')
                    if IOrganization.providedBy(value):
                        html += value.Title()
                elif col == 'photo':
                    photo = getattr(result, col, '')
                    if isinstance(photo, Image):
                        html += result.tag(scale='thumb')
                elif col == 'birthdate':
                    msg = result.getField('birthdate').getLocalized(result)
                    if msg:
                        html += translate(msg, context=self.request)
                else:
                    html += getattr(result, col, '')
                html += '</span>'
    
                # If the column is the title (Full name), the short name, first
                # name, or last name, i need to wrap it between <a> tags
                if col in ('title', 'shortName', 'firstName', 'lastName'):
                    html = '<a href="%s">%s</a>' % (result.absolute_url(), html)
    
                # If the column is the organization, then i wrap it between
                # <a> tags with the organization's URL
                if col == 'organization':
                    value = getattr(result, col, '')
                    if IOrganization.providedBy(value):
                        html = '<a href="%s">%s</a>' % (value.absolute_url(), html)
                            
                # If the column is the email address (any of them), i need to
                # wrap it between <a> tags with mailto:
                if col in ('email', 'workEmail', 'workEmail2', 'workEmail3'):
                    html = '<a href="mailto:%s">%s</a>' % (getattr(result, col, ''), html)
                            
                # If the column is the phone number (any of them), i need to
                # wrap it between <a> tags with callto:
                if col in ('phone', 'workPhone', 'workPhoneInternal', 'phoneInternal'):
                    html = '<a href="callto:%s">%s</a>' % (getattr(result, col, ''), html)
    
                # If the column is the website field, i need also <a> tags
                if col == 'web':
                    html = '<a href="%s">%s</a>' % (getattr(result, col, ''), html)
                    
                if col == 'members':
                    html = len(result.persons)
    
                row.append(html)
            rows.append({'object': result,
                         'cells': row})
        return rows
    

class PersonTable(AbstractTable):
    """ Lists persons
    """
    implements(ITable)
    name = "person"
    default_sort = (('sortable_title', 'asc'),)
    attrs = ['shortName',
             'firstName',
             'lastName',
             'birthdate',
             'organization',
             'position',
             'department',
             'workPhone',
             'workMobilePhone',
             'workEmail',
             'address',
             'city',
             'zip',
             'country',
             'state',
             'phone',
             'mobilePhone',
             'email',
             'web',
             'text',
             'SearchableText',]
            
    def newSearch(self):
        return self.request.get('form.actions.label_search_persons', None) is not None or \
               self.request.get('quicksearch', None) is not None
    
    def email(self, person):
        return person.email or person.workEmail or person.workEmail2 or person.workEmail3 or None

class OrganizationTable(AbstractTable):
    """ Lists organizations
    """
    implements(ITable)
    name = "organization"
    default_sort = (('sortable_title', 'asc'),)
    attrs = ['title',
             'address',
             'city',
             'zip',
             'extraAddress',
             'phone',
             'fax',
             'email',
             'email2',
             'email3',
             'web',
             'text',
             'country',
             'state',
             'sector',
             'sub_sector',
             'SearchableText',]
            
    def newSearch(self):
        return self.request.get('form.actions.label_search_organizations', None) is not None or \
               self.request.get('quicksearch', None) is not None
    
    def email(self, organization):
        return organization.email or organization.email2 or organization.email3 or None

class GroupTable(AbstractTable):
    """ Lists groups
    """
    implements(ITable)
    name = "group"
    default_sort = (('sortable_title', 'asc'),)
    attrs = ['SearchableText',]
            
    def newSearch(self):
        return self.request.get('quicksearch', None) is not None
    
    def email(self, group):
        emails = []
        persons = group.persons
        for person in persons:
            email = person.email or person.workEmail or person.workEmail2 or person.workEmail3 or None
            if email is not None:
                emails.append(email)
        return ', '.join(emails)
