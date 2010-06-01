from Acquisition import aq_inner, aq_parent

from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFPlone.PloneBatch import Batch

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.interfaces import IAddressBook, ITable
from collective.contacts import contactsMessageFactory as _
from collective.contacts.export import exportPersons, exportOrganizations

class AbstractListView(BrowserView):
    template = ViewPageTemplateFile('./templates/list.pt')
    table_template = ViewPageTemplateFile('./templates/table.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.table = getMultiAdapter((self.context, self.request), interface=ITable, name=self.name)
        
    def __call__(self):
        self.error = None
        rows = self.table.rows()
        if not rows:
            self.error = self.error_msg
        self.batch = Batch(rows, self.page_size, self.request.form.get('b_start', 0))
        return self.template()
    
    def canExport(self):
        return not self.name == 'group'
    
    def canImport(self):
        parent = aq_inner(self.context)
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return _checkPermission(ModifyPortalContent, parent)
    
    def hasAdvancedSearch(self):
        return not self.name == 'group'
    
    def customize_url(self):
        if self.name == 'group':
            return None
        if not _checkPermission(ModifyPortalContent, aq_inner(self.context)):
            return None
        return '%s/customize?customize.type=%s' % (self.context.absolute_url(), self.name)
    
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
    template_id = 'persons'
    name = 'person'
    page_size = 20
    error_msg = _('no_persons', default=u'There are no persons available')
    title = _('Persons')

class OrganizationListView(AbstractListView):
    """ Lists organizations
    """
    template_id = 'organizations'
    name = 'organization'
    page_size = 20
    error_msg = _('no_organizations', default=u'There are no organizations available')
    title = _('Organizations')

class GroupListView(AbstractListView):
    """ Lists groups
    """
    template_id = 'groups'
    name = 'group'
    page_size = 20
    error_msg = _('no_groups', default=u'There are no groups available')
    title = _('Groups')
