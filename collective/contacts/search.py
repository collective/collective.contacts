from Acquisition import aq_inner, aq_parent

from zope.interface import implements, Interface
from zope.component import adapts

from Products.CMFCore.utils import getToolByName

from collective.contacts.interfaces import ISearch, IGroup, IPerson, IAddressBook, IOrganization

class Search(object):
    """ Searches the portal
    """
    implements(ISearch)
    _marker = []
    
    def __init__(self, context):
        self.context = context
        
    def filter(self, o, query):
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
    
    def additional_query(self):
        return {}
    
    def object_provides(self):
        return Interface.__identifier__

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
        # add object provides to catalog query
        catalog['object_provides'] = self.object_provides()
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
    """ Searches address books
    """
    adapts(IAddressBook)
    def additional_query(self):
        return {'path': '/'.join(self.context.getPhysicalPath())}

class AddressBookPersonSearch(AddressBookSearch):
    """ Searches persons in address books
    """
    def object_provides(self):
        return IPerson.__identifier__

class AddressBookOrganizationSearch(AddressBookSearch):
    """ Searches organizations in address books
    """
    def object_provides(self):
        return IOrganization.__identifier__

class AddressBookGroupSearch(AddressBookSearch):
    """ Searches groups in address books
    """
    def object_provides(self):
        return IGroup.__identifier__ 

class OrganizationPersonSearch(Search):
    """ Searches persons in organizations
    """
    def additional_query(self):
        # find address book
        parent = aq_parent(aq_inner(self.context))
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return {'path': '/'.join(parent.getPhysicalPath()),
                'organization': self.context.UID()}
    def object_provides(self):
        return IPerson.__identifier__

class OrganizationGroupSearch(Search):
    """ Searches groups in organizations
    """
    adapts(IOrganization)
    def additional_query(self):
        return {'path': {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}}
    def object_provides(self):
        return IGroup.__identifier__ 

class GroupPersonSearch(Search):
    """ Searches persons in groups
    """
    adapts(IGroup)
    def additional_query(self):
        # if we have no persons return the groups UID to force an empty result set
        if not self.context.persons:
            return {'UID': self.context.UID()}
        # find address book
        parent = aq_parent(aq_inner(self.context))
        while not IAddressBook.providedBy(parent):
            parent = aq_parent(parent)
        return {'path': '/'.join(parent.getPhysicalPath()),
                'UID': [person.UID() for person in self.context.persons]}
    def object_provides(self):
        return IPerson.__identifier__ 

class GroupGroupSearch(Search):
    """ Searches groups in groups
    """
    adapts(IGroup)
    def additional_query(self):
        return {'path': {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}}
    def object_provides(self):
        return IGroup.__identifier__ 
    