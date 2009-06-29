# -*- coding: utf-8 -*-
from plone.memoize.instance import memoize

from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts import contactsMessageFactory as _

from collective.contacts.export import exportPersons

from collective.contacts.content.organization import Organization
from collective.contacts.content.person import Person
from Products.Archetypes.Field import Image

@memoize
def get_countries_vocab(person):
    return person.getField('country').Vocabulary()

@memoize
def get_states_vocab(person):
    return person.getField('state').Vocabulary()

class IAddressPersonsView(Interface):
    """
    AddressPersons view interface
    """

    def get_persons():
        """
        This method returns all persons inside this address book
        """
        
    def get_table_headers():
        """
        This method returns a list with the headers for each column
        """

    def get_table_rows():
        """
        This method returns a list with the content for each row, for the given
        person.
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

    def get_table_headers(self):
        """
        This method returns a list with the headers for each column
        """

        results = []
        schema = Person.schema

        for i in self.context.show_on_persons_view:
            if i[1]:
                results.append(schema.get(i[0]).widget.label)

        return results

    def get_table_rows(self, person):
        """
        This method returns a list with the content for each row, for the given
        person.
        """

        #XXX: For some unknown reason, when this product was first developed
        # i used different names for the fields than the ones from the
        # schemas, so i need to do this ugly thing here. This should be
        # removed when we have some unit tests and we can safely change
        # the field names
        match_field ={'title':'title',
                      'shortName':'short_name',
                      'firstName':'first_name',
                      'lastName':'last_name',
                      'organization':'organization',
                      'position':'position',
                      'department':'department',
                      'workPhone':'work_phone',
                      'workMobilePhone':'work_mobile_phone',
                      'workEmail':'work_email',
                      'phone':'phone',
                      'mobilePhone':'mobile_phone',
                      'email':'email',
                      'web':'web',
                      'address':'address',
                      'city':'city',
                      'country':'country',
                      'state':'state',
                      'workEmail2':'work_email2',
                      'workEmail3':'work_email3',
                      'photo':'photo',
                      'text':'text'}
                       
        results = []

        for i in self.context.show_on_persons_view:
            if i[1]:
                html =''
                html += '<span>'
                if i[0] == 'country':
                    vocab = get_countries_vocab(person)
                    value = vocab.getValue(person.country)
                    if value:
                        html += value
                elif i[0] == 'state':
                    vocab = get_states_vocab(person)
                    value = vocab.getValue(person.state)
                    if value:
                        html += value
                elif i[0] == 'organization':
                    value = getattr(person, i[0], '')
                    if isinstance(value, Organization):
                        html += value.Title()
                elif i[0] == 'photo':
                    photo = getattr(person, match_field[i[0]], '')
                    if isinstance(photo, Image):
                        html += person.tag(scale='thumb')
                else:
                    html += getattr(person, match_field[i[0]], '')
                html += '</span>'

                # If the column is the title (Full name), the short name, first
                # name, or last name, i need to wrap it between <a> tags
                if i[0] == 'title' or\
                   i[0] == 'shortName' or\
                   i[0] == 'firstName' or\
                   i[0] == 'lastName':
                    html = ('<a href="' + person.absolute_url() + '">' +
                            html + '</a>')

                # If the column is the organization, then i wrap it between
                # <a> tags with the organization's URL
                if i[0] == 'organization':
                    value = getattr(person, i[0], '')
                    if isinstance(value, Organization):
                        html = ('<a href="' + value.absolute_url() + '">' +
                            html + '</a>')
                            
                # If the column is the email address (any of them), i need to
                # wrap it between <a> tags with mailto:
                if i[0] == 'email' or\
                   i[0] == 'workEmail' or\
                   i[0] == 'workEmail2' or\
                   i[0] == 'workEmail3':
                    html = ('<a href="mailto:' + getattr(person,\
                                                         match_field[i[0]],\
                                                         '')\
                                                        +'">' + html + '</a>')

                # If the column is the website field, i need also <a> tags
                if i[0] == 'web':
                    html = ('<a href="' + getattr(person,\
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