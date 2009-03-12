from zope.interface import implements, Interface
from zope.interface import implements, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _


class IAddressGroupsView(Interface):
    """
    AddressGroups view interface
    """

    def get_groups():
        """
        This method returns all groups inside this address book
        """

    def test():
        """method that does the same as test on old page templates"""


class AddressGroupsView(BrowserView):
    """
    AddressGroups browser view
    """
    implements(IAddressGroupsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # This is needed so the actions bar will be shown.
        # the one with the actions, display, add item and workflow drop downs.
        alsoProvides(self, IViewView)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_groups(self):
        """
        This method returns all groups inside this address book
        """
        groups = []
        for i in self.context.getChildNodes():
            if i.portal_type == 'Group':
                groups.append(i)

        return groups

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
