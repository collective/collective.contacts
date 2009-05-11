# -*- coding: utf-8 -*-
from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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

    pt = ViewPageTemplateFile('templates/addressgroupsview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        # This is needed so the actions bar will be shown.
        # the one with the actions, display, add item and workflow drop downs.
        portal_membership = getToolByName(self.context, 'portal_membership')
        if not portal_membership.isAnonymousUser():
            alsoProvides(self, IViewView)

        return self.pt()
    
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
        brains = self.portal_catalog({'portal_type':'Group',
                             'path':'/'.join(self.context.getPhysicalPath()),
                             'sort_on':'sortable_title'})

        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        groups = [i.getObject() for i in brains]

        return groups

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
