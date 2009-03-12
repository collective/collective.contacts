from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.export import exportPersons, exportOrganizations


class IAddressView(Interface):
    """
    Address view interface
    """

    def search_persons():
        """
        This method returns all persons inside this address book
        """

    def search_organizations():
        """
        This method returns all organizations inside this address book
        """

    def test():
        """method that does the same as test on old page templates"""


class AddressView(BrowserView):
    """
    Address browser view
    """
    implements(IAddressView)

    pt = ViewPageTemplateFile('./addressview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
            """
            This method gets called everytime the template needs to be rendered
            """

            form = self.request.form
            path = '/'.join(self.context.getPhysicalPath())

            # Here we know if the user requested to export the users
            # or export the organizations.
            export_persons = form.get('form.button.export_persons', False)
            export_organizations = form.get('form.button.export_org', False)

            # This is necessary in case this method gets called and no button was
            # pressed. In that case it will just render the template

            if export_persons or export_organizations:
                # In any case we ask for the user selection
                # Now the selections come in a list formed of the id's and the
                # emails, using a space as a separator, so we now separate them

                if export_persons:
                    # If the export action was requested we will be using the
                    # users selections to first filter and then we provide
                    # a download dialog. The export will be done in csv format
                    return exportPersons(self.context,
                                         self.request,
                                         path,
                                         format='csv')

                if export_organizations:
                    # If the export action was requested we will be using the
                    # users selections to first filter and then we provide
                    # a download dialog. The export will be done in csv format
                    return exportOrganizations(self.context,
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

    def search_persons(self):
        """
        This method returns all persons inside this address book
        """
        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        persons =[i.getObject() for i in self.portal_catalog(
                               {'portal_type':'Person',
                                'path':'/'.join(self.context.getPhysicalPath()),
                                'sort_on':'id'
                                })]
        
        return persons

    def search_organizations(self):
        """
        This method returns all organizations inside this address book
        """
        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        organizations = [i.getObject() for i in self.portal_catalog(
                            {'portal_type':'Organization',
                                'path':'/'.join(self.context.getPhysicalPath()),
                                'sort_on':'sortable_title'
                                })]

        return organizations

    def search_groups(self):
        """
        This method returns all groups inside this address book
        """
        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        groups = [i.getObject() for i in self.portal_catalog(
                                {'portal_type':'Group',
                                 'path':'/'.join(self.context.getPhysicalPath()),
                                 'sort_on':'sortable_title'
                                 })]

        return groups

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
