from Acquisition import aq_inner, aq_parent

from zope.i18n import translate
from zope.interface import implements
from zope.component import getMultiAdapter, getAdapters, queryMultiAdapter
from plone.memoize.instance import memoize
from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFPlone.PloneBatch import Batch

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.interfaces import IAddressBook, ITable, IExport, ICustomizableView
from collective.contacts import contactsMessageFactory as _

class AbstractListView(BrowserView):
    implements(ICustomizableView)
    template = ViewPageTemplateFile('./templates/list.pt')
    table_template = ViewPageTemplateFile('./templates/table.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.table = getMultiAdapter((self.context, self.request), interface=ITable, name=self.name)
        
    def __call__(self):
        self.error = None
        self.table.reset()
        rows = self.table.rows()
        if not rows:
            self.error = self.error_msg
        self.batch = Batch(rows, self.page_size, self.request.form.get('b_start', 0))
        return self.template()
    
    @memoize
    def exportFormats(self):
        def format_cmp(x, y):
            return cmp(x['title'], y['title'])
        formats = [{'value': name,
                    'title': translate(adapter.title, context=self.request)} for name, adapter in getAdapters((self.context,), IExport) if name.startswith('%s.' % self.name)]
        formats.sort(format_cmp)
        return formats
    
    @memoize
    def canImport(self):
        if self.name == 'group':
            return
        parent = aq_inner(self.context)
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return _checkPermission(ModifyPortalContent, parent)
    
    @memoize
    def advanced_url(self):
        if queryMultiAdapter((self.context, self.request), name='find_%s' % self.name) is None:
            return None
        return '%s/find_%s' % (self.context.absolute_url(), self.name)
    
    @memoize
    def customize_url(self):
        if self.name == 'group':
            return None
        if not _checkPermission(ModifyPortalContent, aq_inner(self.context)):
            return None
        return '%s/customize?customize.type=%s' % (self.context.absolute_url(), self.name)
    
    @memoize
    def search_url(self):
        return '%s/search_%s' % (self.context.absolute_url(), self.name)
    
    @memoize
    def results(self):
        if not self.table:
            return None
        return self.table_template(table=self.table, batch=self.batch)

class PersonListView(AbstractListView):
    """ Lists persons
    """
    implements(IViewView)
    template_id = 'persons'
    name = 'person'
    page_size = 20
    error_msg = _('no_persons', default=u'There are no persons available')
    title = _('Persons')

class OrganizationListView(AbstractListView):
    """ Lists organizations
    """
    implements(IViewView)
    template_id = 'organizations'
    name = 'organization'
    page_size = 20
    error_msg = _('no_organizations', default=u'There are no organizations available')
    title = _('Organizations')

class GroupListView(AbstractListView):
    """ Lists groups
    """
    implements(IViewView)
    template_id = 'groups'
    name = 'group'
    page_size = 20
    error_msg = _('no_groups', default=u'There are no groups available')
    title = _('Groups')
