from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore.permissions import ModifyPortalContent

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import ITable
from collective.contacts.export import exportPersons, exportOrganizations

class AbstractSearchView(BrowserView):
    """ Displays search results
    """

    template = ViewPageTemplateFile('./templates/search.pt')
    table_template = ViewPageTemplateFile('./templates/table.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def __call__(self):
        # redirect on import
        if self.request.get('form.button.import', None) is not None:
            parent = aq_inner(self.context)
            while not IAddressBook.providedBy(parent):
                parent = aq_parent(parent)
            if not _checkPermission(ModifyPortalContent, parent):
                return None
            return '%s/import_view' % parent.absolute_url()
        
        self.error = None
        self.quick = self.request.get('quicksearch', None) is not None
        mail = self.request.get('form.button.mailto', None) is not None
        export = self.request.get('form.button.export', None) is not None
        exportall = self.request.get('form.button.exportall', None) is not None
        advanced = self.request.get('form.button.advanced', None) is not None
        
        self.table = getMultiAdapter((self.context, self.request), interface=ITable, name=self.name)
        selection = self.get_selection()
        
        if (export or mail) and not selection:
            self.error = _(u'You need to select at least one person or organization')
        elif mail:
            self.mailto = self.get_mailto(selection)
            if not self.mailto.strip():
                self.error = _(u'You need to select at least one person or organization that has an email')
        elif export or exportall:
            if self.name == 'person':
                return exportPersons(self.context, self.request, export and selection or None)
            elif self.name == 'organization':
                return exportOrganizations(self.context, self.request, export and selection or None)
        elif advanced:
            return self.request.RESPONSE.redirect(self.advanced_url)
        
        return self.template()
    
    def get_selection(self):
        if self.request.form.get('selection', None) is None:
            return []
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(UID=self.request.form.get('selection', []))
        return [brain.getObject() for brain in results]
    
    def get_mailto(self, selection):
        emails = []
        for object in selection:
            email = self.table.email(object)
            if email:
                emails.append(email)
        return ', '.join(emails)
    
    @property
    def advanced_url(self):
        if self.name == 'group':
            return None
        return '%s/find_%s' % (self.context.absolute_url(), self.name)
    
    @property
    def search_url(self):
        return '%s/search_%s' % (self.context.absolute_url(), self.name)
    
    @memoize
    def results(self):
        if not self.table:
            return None
        return self.table_template(table=self.table)

class PersonSearchView(AbstractSearchView):
    """ Displays person search results
    """
    name = 'person'

class OrganizationSearchView(AbstractSearchView):
    """ Displays organization search results
    """
    name = 'organization'

class GroupSearchView(AbstractSearchView):
    """ Displays group search results
    """
    name = 'group'
