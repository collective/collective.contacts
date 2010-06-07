from Acquisition import aq_inner, aq_parent
from AccessControl import Unauthorized

from zope.component import getMultiAdapter, queryAdapter, queryMultiAdapter, getAdapters
from plone.memoize.instance import memoize

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFPlone.PloneBatch import Batch

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.interfaces import ITable, IAddressBook, IExport
from collective.contacts import contactsMessageFactory as _

class AbstractSearchView(BrowserView):
    """ Displays search results
    """

    template = ViewPageTemplateFile('./templates/search.pt')
    table_template = ViewPageTemplateFile('./templates/table.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def __call__(self):
        self.request.set('disable_border', 1)
        # redirect on import
        if self.request.get('form.button.import', None) is not None:
            parent = aq_inner(self.context)
            while not IAddressBook.providedBy(parent):
                parent = aq_parent(parent)
            if not _checkPermission(ModifyPortalContent, parent):
                raise Unauthorized
            return self.request.response.redirect('%s/import' % parent.absolute_url())
        
        self.error = None
        self.quick = self.request.get('quicksearch', None) is not None
        mail = self.request.get('form.button.mailto', None) is not None
        export = self.request.get('form.button.export', None) is not None
        exportall = self.request.get('form.button.exportall', None) is not None
        exportsearch = self.request.get('form.button.exportsearch', None) is not None
        exportformat = self.request.get('form.exportformat', 'csv')
        advanced = self.request.get('form.button.advanced', None) is not None
        
        self.table = getMultiAdapter((self.context, self.request), interface=ITable, name=self.name)
        rows = self.table.rows()
        self.batch = Batch(rows, self.page_size, self.request.form.get('b_start', 0))
        
        selection = self.get_selection()
        
        if (export or mail) and not selection:
            self.error = _(u'You need to select at least one person or organization')
        elif mail:
            self.mailto = self.get_mailto(selection)
            if not self.mailto.strip():
                self.error = _(u'You need to select at least one person or organization that has an email')
        elif export or exportall or exportsearch:
            if exportsearch:
                selection = [row['object'] for row in rows]
            handler = queryAdapter(self.context, interface=IExport, name=exportformat)
            if handler is None:
                handler = queryAdapter(self.context, interface=IExport, name='%s.csv' % self.name)
            return handler.export(self.request, (export or exportsearch) and selection or None)
        elif advanced:
            return self.request.RESPONSE.redirect(self.advanced_url)
        
        return self.template()
    
    @memoize
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
                emails.extend(email.split(', '))
        return ', '.join(set(emails))
    
    @memoize
    def exportFormats(self):
        return [{'value': name,
                 'title': adapter.title} for name, adapter in getAdapters((self.context,), IExport) if name.startswith('%s.' % self.name)]
    
    @property
    @memoize
    def advanced_url(self):
        if queryMultiAdapter((self.context, self.request), name='find_%s' % self.name) is None:
            return None
        return '%s/find_%s' % (self.context.absolute_url(), self.name)
    
    @property
    @memoize
    def search_url(self):
        return '%s/search_%s' % (self.context.absolute_url(), self.name)
    
    @memoize
    def results(self):
        if not self.table:
            return None
        return self.table_template(table=self.table, batch=self.batch)

class PersonSearchView(AbstractSearchView):
    """ Displays person search results
    """
    template_id = 'search_person'
    name = 'person'
    page_size = 20

class OrganizationSearchView(AbstractSearchView):
    """ Displays organization search results
    """
    template_id = 'search_organization'
    name = 'organization'
    page_size = 20

class GroupSearchView(AbstractSearchView):
    """ Displays group search results
    """
    template_id = 'search_group'
    name = 'group'
    page_size = 20
