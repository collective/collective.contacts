# -*- coding: utf-8 -*-
from plone.memoize.instance import memoize

from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts import contactsMessageFactory as _

from collective.contacts.export import exportOrganizations

from collective.contacts.content.organization import Organization

@memoize
def get_countries_vocab(organization):
    return organization.getField('country').Vocabulary()

@memoize
def get_states_vocab(organization):
    return organization.getField('state').Vocabulary()


class IAddressOrganizationsView(Interface):
    """
    AddressOrganizations view interface
    """

    def get_organizations():
        """
        This method returns all organizations inside this address book
        """

    def get_table_headers():
        """
        This method returns a list with the headers for each column
        """
        
    def get_table_rows():
        """
        This method returns a list with the content for each row, for the given
        organization.
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
        brains = self.portal_catalog({'portal_type':'Organization',
                             'path':'/'.join(self.context.getPhysicalPath()),
                             'sort_on':'sortable_title'})
                             
        # XXX: This getObject should be removed and done in a way
        # that we can ask the data from the catalog instead of getting
        # all the objects.
        organizations = [i.getObject() for i in brains]

        return organizations

    def get_table_headers(self):
        """
        This method returns a list with the headers for each column
        """
        
        results = []
        schema = Organization.schema
       
        for i in self.context.show_on_organizations_view:
            if i[1]:
                results.append(schema.get(i[0]).widget.label)
            
        return results

    def get_table_rows(self, organization):
        """
        This method returns a list with the content for each row, for the given
        organization.
        """

        #XXX: For some unknown reason, when this product was first developed
        # i used different names for the fields than the ones from the
        # schemas, so i need to do this ugly thing here. This should be
        # removed when we have some unit tests and we can safely change
        # the field names
        match_field ={'title':'title',
                      'sector':'sector',
                      'sub_sector':'sub_sector',
                      'phone':'phone',
                      'fax':'fax',
                      'email':'email',
                      'web':'web',
                      'address':'address',
                      'city':'city',
                      'country':'country',
                      'description':'description',
                      'state':'state',
                      'zip':'zip',
                      'extraAddress':'extra_address',
                      'email2':'email2',
                      'email3':'email3',
                      'text':'text'}
            
        results = []

        for i in self.context.show_on_organizations_view:
            if i[1]:
                html =''
                html += '<span>'
                if i[0] == 'country':
                    vocab = get_countries_vocab(organization)
                    value = vocab.getValue(organization.country)
                    if value:
                        html += value
                elif i[0] == 'state':
                    vocab = get_states_vocab(organization)
                    value = vocab.getValue(organization.state)
                    if value:
                        html += value
                else:
                    html += getattr(organization, match_field[i[0]], '')
                html += '</span>'

                # If the column is the title, i need to wrap it between <a> tags
                if i[0] == 'title':
                    html = ('<a href="' + organization.absolute_url() + '">' +
                            html + '</a>')

                # If the column is the email address, i need to wrap it between <a>
                # tags with mailto:
                if i[0] == 'email':
                    html = ('<a href="mailto:' + getattr(organization,\
                                                         match_field[i[0]],\
                                                        '')\
                                                        +'">' + html + '</a>')

                # If the column is the website field, i need also <a> tags
                if i[0] == 'web':
                    html = ('<a href="' + getattr(organization,\
                                                  match_field[i[0]],\
                                                  '')\
                                                  + '">' + html + '</a>')

                results.append(html)

        return results

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
