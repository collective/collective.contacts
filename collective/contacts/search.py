from Acquisition import aq_inner, aq_parent

from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName

from collective.contacts.interfaces import ISearch, IGroup, IAddressBook, IOrganization

class Search(object):
    """ Searches the portal
    """
    implements(ISearch)
    _marker = []
    
    def __init__(self, context):
        self.context = context
        
    def filter(self, o, query):
        if not self.custom_filter(o, query):
            return False
        for attr, value in query.items():
            data = getattr(o, attr, self._marker)
            if data is self._marker:
                return False
            try:
                # try to convert to string
                data = str(data)
            except:
                try:
                    # try to get the title
                    data = str(data.Title())
                except:
                    data = ''
            if value.lower() not in data.lower():
                return False
        return True
        
    def custom_filter(self, o, query):
        return True
    
    def additional_query(self):
        return {}

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def search(self, query={}, sort='sortable_title'):
        """ Search for items matching the values
        """
        query.update(self.additional_query())
        indexes = self.portal_catalog.indexes()
        filter = {}
        catalog = {}
        for key, value in query.items():
            if not value or (value == '--' and key in ('state', 'country', 'sector', 'sub_sector',)):
                continue
            if key in indexes:
                catalog[key] = value
            else:
                filter[key] = value
        # modifying the search string so the search is able to return
        # a result, even if no full word is provided
        if catalog.has_key('SearchableText'):
            catalog['SearchableText'] = '* OR '.join(catalog['SearchableText'].lower().split())+'*'
        # check whether the sort parameter is a string and use the ordinary catalog
        # search or it is not and we need to use advanced query for sorting
        if isinstance(sort, basestring):
            catalog['sort_on'] = sort
            brains = self.portal_catalog(catalog)
        else:
            brains = self.portal_catalog.evalAdvancedQuery(self.portal_catalog.makeAdvancedQuery(catalog), 
                                                           sort)
        # filter out objects not matching the values
        filtered = []
        for brain in brains:
            o = brain.getObject()
            if not self.filter(o, filter):
                continue
            filtered.append(o)
        return filtered

class AddressBookSearch(Search):
    """ Searches an address book
    """
    adapts(IAddressBook)
    
    def additional_query(self):
        return {'path': '/'.join(self.context.getPhysicalPath())}
    
class OrganizationSearch(Search):
    """ Searches in an organization
    """
    adapts(IOrganization)
    
    def additional_query(self):
        # find address book
        parent = aq_parent(aq_inner(self.context))
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return {'path': '/'.join(parent.getPhysicalPath())}
    
    def custom_filter(self, o, query):
        return o.organization and o.organization.getId() == self.context.getId()

class GroupSearch(Search):
    """ Searches in a group
    """
    adapts(IGroup)
    
    @property
    def group_persons(self):
        return self.context.persons
    
    def additional_query(self):
        # find address book
        parent = aq_parent(aq_inner(self.context))
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return {'path': '/'.join(parent.getPhysicalPath())}
    
    def custom_filter(self, o, query):
        return o in self.context.persons
    