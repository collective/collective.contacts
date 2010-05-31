from Acquisition import aq_inner, aq_parent

from zope.interface import implements
from zope.component import adapts, getAdapter, getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFPlone.PloneBatch import Batch

from collective.contacts.interfaces import ITable, ICustomizableColumns, IPerson, IOrganization, IGroup, ISearch

class PersonTable(object):
    """ Lists persons
    """
    implements(ITable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cols = getAdapter(self.context, interface=ICustomizableColumns, name='person')
        self.sort = (('lastName', 'asc'),
                     ('firstName', 'asc'))
        
    def set_sort(self, sort):
        self.sort = sort
        
    def columns(self):
        return [self.cols.translate_column(column) for column in self.cols.get_columns()]
    
    def rows(self):
        attrs = {'short_name' : self.request.get('short_name', None),
                 'first_name' : self.request.get('first_name', None),
                 'last_name' : self.request.get('last_name', None),
                 'organization' : self.request.get('organization', None),
                 'position' : self.request.get('position', None),
                 'department' : self.request.get('department', None),
                 'work_phone' : self.request.get('work_phone', None),
                 'work_mobile_phone' : self.request.get('work_mobile_phone', None),
                 'work_email' : self.request.get('work_email', None),
                 'address' : self.request.get('address', None),
                 'city' : self.request.get('city', None),
                 'zip' : self.request.get('zip', None),
                 'country' : self.request.get('country', None),
                 'state' : self.request.get('state', None),
                 'phone' : self.request.get('phone', None),
                 'mobile_phone' : self.request.get('mobile_phone', None),
                 'email' : self.request.get('email', None),
                 'web' : self.request.get('web', None),
                 'text' : self.request.get('text', None),
                 'SearchableText' : self.request.get('SearchableText', None),
                 'object_provides': IPerson.__identifier__,
        }
        search = ISearch(self.context)
        results = search.search(query=attrs, sort=self.sort)
        if not results:
            return []
    
        #XXX: For some unknown reason, when this product was first developed
        # i used different names for the fields than the ones from the
        # schemas, so i need to do this ugly thing here. This should be
        # removed when we have some unit tests and we can safely change
        # the field names
        match_field ={'title':'title',
                      'shortName':'short_name',
                      'firstName':'first_name',
                      'lastName':'last_name',
                      'organization':'organization',
                      'position':'position',
                      'department':'department',
                      'workPhone':'work_phone',
                      'workMobilePhone':'work_mobile_phone',
                      'workEmail':'work_email',
                      'phone':'phone',
                      'mobilePhone':'mobile_phone',
                      'email':'email',
                      'web':'web',
                      'address':'address',
                      'city':'city',
                      'zip':'zip',
                      'country':'country',
                      'state':'state',
                      'workEmail2':'work_email2',
                      'workEmail3':'work_email3',
                      'photo':'photo',
                      'text':'text'}
    
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
                    photo = getattr(result, match_field[col], '')
                    if isinstance(result, Image):
                        html += result.tag(scale='thumb')
                else:
                    html += getattr(result, match_field[col], '')
                html += '</span>'
    
                # If the column is the title (Full name), the short name, first
                # name, or last name, i need to wrap it between <a> tags
                if col == 'title' or\
                   col == 'shortName' or\
                   col == 'firstName' or\
                   col == 'lastName':
                    html = ('<a href="' + result.absolute_url() + '">' +
                            html + '</a>')
    
                # If the column is the organization, then i wrap it between
                # <a> tags with the organization's URL
                if col == 'organization':
                    value = getattr(result, col, '')
                    if IOrganization.providedBy(value):
                        html = ('<a href="' + value.absolute_url() + '">' +
                            html + '</a>')
                            
                # If the column is the email address (any of them), i need to
                # wrap it between <a> tags with mailto:
                if col == 'email' or\
                   col == 'workEmail' or\
                   col == 'workEmail2' or\
                   col == 'workEmail3':
                    html = ('<a href="mailto:' + getattr(result,\
                                                         match_field[col],\
                                                         '')\
                                                        +'">' + html + '</a>')
    
                # If the column is the website field, i need also <a> tags
                if col == 'web':
                    html = ('<a href="' + getattr(result,\
                                                         match_field[col],\
                                                         '')\
                                                       + '">' + html + '</a>')
    
                row.append(html)
            rows.append({'object': result,
                         'cells': row})
        return rows
    
    def email(self, person):
        return person.email or person.work_email or person.work_email2 or person.work_email3 or None

class OrganizationTable(object):
    """ Lists organizations
    """
    implements(ITable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cols = getAdapter(self.context, interface=ICustomizableColumns, name='organization')
        self.sort = 'sortable_title'
        
    def set_sort(self, sort):
        self.sort = sort
        
    def columns(self):
        return [self.cols.translate_column(column) for column in self.cols.get_columns()]
    
    def rows(self, sort='sortable_title'):
        attrs = {'title' : self.request.get('title', None),
                 'address' : self.request.get('address', None),
                 'city' : self.request.get('city', None),
                 'zip' : self.request.get('zip', None),
                 'extra_adress' : self.request.get('extra_adress', None),
                 'phone' : self.request.get('phone', None),
                 'fax' : self.request.get('fax', None),
                 'email' : self.request.get('email', None),
                 'email2' : self.request.get('email2', None),
                 'email3' : self.request.get('email3', None),
                 'web' : self.request.get('web', None),
                 'text' : self.request.get('text', None),
                 'SearchableText' : self.request.get('SearchableText', None),
                 'object_provides': IOrganization.__identifier__,
                }
        search = ISearch(self.context)
        results = search.search(query=attrs, sort=self.sort)
        if not results:
            return []

        #XXX: For some unknown reason, when this product was first developed
        # i used different names for the fields than the ones from the
        # schemas, so i need to do this ugly thing here. This should be
        # removed when we have some unit tests and we can safely change
        # the field names
        match_field ={'title':'title',
                      'sector':'sector',
                      'sub_sector':'sub_sector',
                      'phone':'phone',
                      'fax':'fax',
                      'email':'email',
                      'web':'web',
                      'address':'address',
                      'city':'city',
                      'country':'country',
                      'description':'description',
                      'state':'state',
                      'zip':'zip',
                      'extraAddress':'extra_address',
                      'email2':'email2',
                      'email3':'email3',
                      'text':'text'}
    
        columns = self.cols.get_columns()
        countries = getUtility(IVocabularyFactory, name='contacts.countries')(self.context)
        states = getUtility(IVocabularyFactory, name='contacts.states')(self.context)
        rows = []
        for result in results:
            row = []
            for col in columns:
                html =''
                html += '<span>'
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
                else:
                    html += getattr(result, match_field[col], '')
                html += '</span>'
    
                # If the column is the title, i need to wrap it between <a> tags
                if col == 'title':
                    html = ('<a href="' + result.absolute_url() + '">' +
                            html + '</a>')
    
                # If the column is the email address, i need to wrap it between <a>
                # tags with mailto:
                if col == 'email':
                    html = ('<a href="mailto:' + getattr(result,\
                                                         match_field[col],\
                                                        '')\
                                                        +'">' + html + '</a>')
    
                # If the column is the website field, i need also <a> tags
                if col == 'web':
                    html = ('<a href="' + getattr(result,\
                                                  match_field[col],\
                                                  '')\
                                                  + '">' + html + '</a>')
    
                row.append(html)
            rows.append({'object': result,
                         'cells': row})
        return rows
    
    def email(self, organization):
        return organization.email or organization.email2 or organization.email3 or None

class GroupTable(object):
    """ Lists groups
    """
    implements(ITable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cols = getAdapter(self.context, interface=ICustomizableColumns, name='group')
        self.sort = 'sortable_title'
        
    def set_sort(self, sort):
        self.sort = sort
        
    def columns(self):
        return [self.cols.translate_column(column) for column in self.cols.get_columns()]
    
    def rows(self):
        attrs = {'SearchableText' : self.request.get('SearchableText', None),
                 'object_provides': IGroup.__identifier__,
                }
        search = ISearch(self.context)
        results = search.search(query=attrs, sort=self.sort)
        if not results:
            return []
    
        rows = []
        for result in results:
            row = ['<a href="%s">%s</a>' % (result.absolute_url(), result.title),
                   len(result.persons)]
            rows.append({'object': result,
                         'cells': row})
        return rows
    
    def email(self, group):
        emails = []
        persons = group.persons
        for person in persons:
            email = person.email or person.work_email or person.work_email2 or person.work_email3 or None
            if email is not None:
                emails.append(email)
        return ', '.join(emails)
