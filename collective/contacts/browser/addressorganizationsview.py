from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts import contactsMessageFactory as _

from collective.contacts.export import exportOrganizations

class IAddressOrganizationsView(Interface):
    """
    AddressOrganizations view interface
    """

    def get_organizations():
        """
        This method returns all organizations inside this address book
        """

    def test():
        """method that does the same as test on old page templates"""


class AddressOrganizationsView(BrowserView):
    """
    AddressOrganizations browser view
    """
    implements(IAddressOrganizationsView)

    pt = ViewPageTemplateFile('templates/addressorganizationsview.pt')

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

        # Here we know if the user requested to export the organizations.
        export_organizations = form.get('form.button.export_org', False)
        # This is necessary in case this method gets called and no button was
        # pressed. In that case it will just render the template
        if export_organizations:
            # If the export action was requested we provide
            # a download dialog. The export will be done in csv format
            return exportOrganizations(self.context,
                                       self.request,
                                       path,
                                       format='csv')


        # XXX: REALLY AWFUL HACK, should be removed when i know how to
        #      have the tab selected when using an action as default view.
#
#        if 'addressorganizations_view' not in self.request.URL:
#            url = self.context.absolute_url() + '/addressorganizations_view'
#            return self.request.response.redirect(url)

        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_organizations(self):
        """
        This method returns all organizations inside this address book
        """
        organizations = []
        for i in self.context.getChildNodes():
            if i.portal_type == 'Organization':
                organizations.append(i)

        return organizations


    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
