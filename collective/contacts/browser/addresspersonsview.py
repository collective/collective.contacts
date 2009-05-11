# -*- coding: utf-8 -*-
from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts import contactsMessageFactory as _

from collective.contacts.export import exportPersons

class IAddressPersonsView(Interface):
    """
    AddressPersons view interface
    """

    def get_persons():
        """
        This method returns all persons inside this address book
        """

    def test():
        """method that does the same as test on old page templates"""

class AddressPersonsView(BrowserView):
    """
    AddressPersons browser view
    """
    implements(IAddressPersonsView)


    pt = ViewPageTemplateFile('templates/addresspersonsview.pt')

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
        
        form = self.request.form
        path = '/'.join(self.context.getPhysicalPath())

        # Here we know if the user requested to export the users
        export_persons = form.get('form.button.export_persons', False)

        # This is necessary in case this method gets called and no button was
        # pressed. In that case it will just render the template
        if export_persons:
            # If the export action was requested we provide
            # a download dialog. The export will be done in csv format
            return exportPersons(self.context,
                                 self.request,
                                 path,
                                 format='csv')

        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_persons(self):
        """
        This method returns all persons inside this address book
        """
        aq = self.portal_catalog.makeAdvancedQuery({'portal_type':'Person',
                             'path':'/'.join(self.context.getPhysicalPath())})

        brains = self.portal_catalog.evalAdvancedQuery(aq,
                                                       (('lastName', 'asc'),
                                                        ('firstName', 'asc'))
                                                        )

        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        persons =[i.getObject() for i in brains]

        return persons

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value