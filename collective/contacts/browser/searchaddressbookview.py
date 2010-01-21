# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.export import exportPersons, exportOrganizations

from ZTUtils import make_query as mq

import zope.i18n

class ISearchAddressBookView(Interface):
    """
    SearchAddressBook view interface
    """

    def test():
        """method that does the same as test on old page templates"""


class SearchAddressBookView(BrowserView):
    """
    SearchAddressBook browser view
    """
    implements(ISearchAddressBookView)

    pt = ViewPageTemplateFile('./templates/searchaddressbookview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        # XXX: This should be reviewed and changed to use portal_form_controller

        form = self.request.form

        if self.context.meta_type == 'Group':
            # Means i'm exporting persons from inside a group. I should form
            # the path from my parent
            path = '/'.join(self.context.aq_inner.aq_parent.getPhysicalPath())
        else:
            path = '/'.join(self.context.getPhysicalPath())

        # Here we know if the user requested to export the users
        # the organizations or to send mails to them.
        mailto = form.get('form.button.mailto', False)
        export_persons = form.get('form.button.export_persons', False)
        export_organizations = form.get('form.button.export_org', False)
        mailto_group = form.get('form.button.mailto_group', False)
        advanced_persons = form.get('form.button.advanced_persons', False)
        advanced_organizations = form.get('form.button.advanced_organizations',
                                          False)

        # This is necessary in case this method gets called and no button was
        # pressed. In that case it will just render the template
        if mailto or export_persons or export_organizations:
            # In any case we ask for the user selection
            # Now the selections come in a list formed of the id's and the
            # emails, using a space as a separator, so we now separate them

            if not form.has_key('user_selection') and not form.has_key('no_mail'):
                aux = _(u'You need to select at least one person or '
                         'organization')
                status = zope.i18n.translate(aux, context=self.request)

                url = self.context.absolute_url() + \
                      '/search_addressbook?error_message=%s' % (status,)
                      
                return self.request.response.redirect(url)
            elif not form.has_key('user_selection') and mailto:
                aux = _(u'You need to select at least one person or '
                         'organization that has an email')
                status = zope.i18n.translate(aux, context=self.request)
                url = self.context.absolute_url() + \
                      '/search_addressbook?error_message=%s' % (status,)

                return self.request.response.redirect(url)
                
            if form.has_key('user_selection'):
                ids = [i.split(' ')[0] for i in form['user_selection']]
                
                if form.has_key('no_mail'):
                    if not isinstance(form['no_mail'], list):
                        ids_nomail = [form['no_mail'].strip()]
                    else:
                        ids_nomail = [i.strip() for i in form['no_mail']]
                    ids = ids + ids_nomail
                    
                mails = [i.split(' ')[1] for i in form['user_selection']]
            else:
                if not isinstance(form['no_mail'], list):
                    ids = [form['no_mail'].strip()]                    
                else:
                    ids = [i.strip() for i in form['no_mail']]

                mails = []

            self.request.string_emails = ', '.join(mails)

            if export_persons:
                # If the export action was requested we will be using the
                # users selections to first filter and then we provide
                # a download dialog. The export will be done in csv format
                return exportPersons(self.context,
                                     self.request,
                                     path,
                                     ids,
                                     'csv')

            if export_organizations:
                # If the export action was requested we will be using the
                # users selections to first filter and then we provide
                # a download dialog. The export will be done in csv format
                return exportOrganizations(self.context,
                                           self.request,
                                           path,
                                           ids,
                                           'csv')
        if mailto_group:
            if not form.has_key('user_selection'):
                aux = _(u'You need to select at least one group')
                status = zope.i18n.translate(aux, context=self.request)
                    
                url = self.context.absolute_url() + \
                      '/search_addressbook?error_message=%s' % (status,)

                return self.request.response.redirect(url)

            resulting_mails = []
            for i in form['user_selection']:
                addresses = i.split(',')
                for i in addresses:
                    if i not in resulting_mails and i != '':
                        resulting_mails.append(i)
                        
            self.request.string_emails = ', '.join(resulting_mails)

            if self.request.string_emails == '':
                aux = _(u'There are no persons to send an email to')
                status = zope.i18n.translate(aux, context=self.request)

                url = self.context.absolute_url() + \
                      '/search_addressbook?error_message=%s' % (status,)

                return self.request.response.redirect(url)

        if advanced_persons:
            url = self.context.absolute_url() + '/personssearch_view'
            return self.request.response.redirect(url)

        if advanced_organizations:
            url = self.context.absolute_url() + '/organizationssearch_view'
            return self.request.response.redirect(url)
        
        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def do_search_organizations(self, request):
        """
        This method will be used to know which method to call,
        the quick or the other one (for organizations).
        """

        quick_search = request.get('quick_organizations_submitted', None)
        advanced_search = request.get('organizations_submitted', None)

        if quick_search and not advanced_search:
            return self.quick_search_organizations(request)

        if not quick_search and advanced_search:
            return self.search_organizations(request)


    def do_search_persons(self, request):
        """
        This method will be used to know which method to call,
        the quick or the other one (for persons).
        """

        quick_search = request.get('quick_persons_submitted', None)
        advanced_search = request.get('persons_submitted', None)

        if quick_search and not advanced_search:
            return self.quick_search_persons(request)

        if not quick_search and advanced_search:
            return self.search_persons(request)

    def do_search_groups(self, request):
        """
        This method will be used to know which method to call,
        the quick or the other one (for groups).
        """

        quick_search = request.get('quick_groups_submitted', None)
        advanced_search = request.get('groups_submitted', None)

        if quick_search and not advanced_search:
            return self.quick_search_groups(request)

        if not quick_search and advanced_search:
            return self.search_groups(request)

    def quick_search_organizations(self, request):
        """
        This method will be used to do a quick search for organizations
        inside an address book.
        """

        # I'm modifying the search string so the search is able to return
        # a result, even if no full word is provided
        search_string = request.get('search_string', '')
        if search_string:
            search_string = '* OR '.join(search_string.split())+'*'

        all_organizations = [i.getObject() for i in self.portal_catalog(
                             {'portal_type':'Organization',
                              'path':'/'.join(self.context.getPhysicalPath()),
                              'SearchableText':search_string,
                               'sort_on':'sortable_title'
                              })]

        return all_organizations


    def search_organizations(self, request):
        """
        This method will be used to search for persons inside an address book
        """

        attrs = {'title' : request.get('title', None),
                 'address' : request.get('address', None),
                 'city' : request.get('city', None),
                 'zip' : request.get('zip', None),
                 'extra_adress' : request.get('extra_adress', None),
                 'phone' : request.get('phone', None),
                 'fax' : request.get('fax', None),
                 'email' : request.get('email', None),
                 'email2' : request.get('email2', None),
                 'email3' : request.get('email3', None),
                 'web' : request.get('web', None),
                 'text' : request.get('text', None),
                }

        
        country = request.get('country', None)
        if country and country != '--':
            attrs['country'] = country
        else:
            attrs['country'] = None

        state = request.get('state', None)
        if state and state != '--':
            attrs['state'] = state
        else:
            attrs['state'] = None

        sector = request.get('sector', None)
        if sector and sector != '--':
            attrs['sector'] = sector
        else:
            attrs['sector'] = None

        sub_sector = request.get('sub_sector', None)
        if sub_sector and sub_sector != '--':
            attrs['sub_sector'] = sub_sector
        else:
            attrs['sub_sector'] = None
            
        all_organizations = [i.getObject() for i in self.portal_catalog(
                               {'portal_type':'Organization',
                                'path':'/'.join(self.context.getPhysicalPath()),
                                'sort_on':'sortable_title'
                               })]
        results = []

        # Now i filter the results
        for organization in all_organizations:
            # I go organization by organization and see
            # if their attributes match with the requested ones.
            exclude = False
            # this exclude variable is a dummy variable i use to
            # know if i should add this organization to the results or not.
            for attr in attrs.keys():
                if attrs[attr] and attrs[attr] != '':
                    # If i'm here means the user entered something to search for
                    # first i need to get the organization's attribute.
                    organization_data = str(getattr(organization, attr, '')).\
                                        lower()

                    if not (attrs[attr].lower() in organization_data):
                        # If i'm here means the data from that organization
                        # is not equal to the one searched.
                        # So i have to exclude this organization
                        exclude = True

            if not exclude:
                if organization not in results:
                    results.append(organization)

        return results

    def quick_search_persons(self, request):
        """
        This method will be used to do a quick search for persons
        inside an address book.
        """

        # I'm modifying the search string so the search is able to return
        # a result, even if no full word is provided
        search_string = request.get('search_string', '')
        if search_string:
            search_string = '* OR '.join(search_string.split())+'*'

        all_persons = [i.getObject() for i in self.portal_catalog(
                             {'portal_type':'Person',
                              'path':'/'.join(self.context.getPhysicalPath()),
                              'SearchableText':search_string,
                               'sort_on':'id'
                              })]
        return all_persons

    def search_persons(self, request):
        """
        This method will be used to search for persons inside an address book
        """

        attrs = {'short_name' : request.get('short_name', None),
                 'first_name' : request.get('first_name', None),
                 'last_name' : request.get('last_name', None),
                 'organization' : request.get('organization', None),
                 'position' : request.get('position', None),
                 'department' : request.get('department', None),
                 'work_phone' : request.get('work_phone', None),
                 'work_mobile_phone' : request.get('work_mobile_phone', None),
                 'work_email' : request.get('work_email', None),
                 'address' : request.get('address', None),
                 'city' : request.get('city', None),
                 'phone' : request.get('phone', None),
                 'mobile_phone' : request.get('mobile_phone', None),
                 'email' : request.get('email', None),
                 'web' : request.get('web', None),
                 'text' : request.get('text', None),
        }
        
        country = request.get('country', None)
        if country and country != '--':
            attrs['country'] = country
        else:
            attrs['country'] = None

        state = request.get('state', None)
        if state and state != '--':
            attrs['state'] = state
        else:
            attrs['state'] = None

        all_persons = [i.getObject() for i in self.portal_catalog(
                              {'portal_type':'Person',
                               'path':'/'.join(self.context.getPhysicalPath()),
                               'sort_on':'id'
                               })]
        results = []

        # Now i filter the results
        for person in all_persons:
            # I go person by person and see if their attributes
            # match with the requested ones.
            exclude = False
            # this exclude variable is a dummy variable i use to know
            # if i should add this person to the results or not.
            for attr in attrs.keys():
                if attrs[attr] and attrs[attr] != '':
                    # If i'm here means the user entered something to search
                    # for first i need to get the person's attribute,
                    # and if the attribute was organization, i need to convert
                    # it to string.
                    if attr == 'organization':
                        organization = getattr(person, attr, '')
                        if organization:
                            organization = str(organization.title)
                        else:
                            organization = ''

                        person_data = organization.lower()
                    else:
                        person_data = str(getattr(person, attr, '')).lower()

                    if not (attrs[attr].lower() in person_data):
                        # If i'm here means the data from that person is not
                        # equal to the one searched.
                        # So i have to exclude this user
                        exclude = True

            if not exclude:
                if person not in results:
                    results.append(person)
                    
        return results

    def quick_search_groups(self, request):
        """
        This method will be used to do a quick search for groups
        inside an address book.
        """
        # I'm modifying the search string so the search is able to return
        # a result, even if no full word is provided
        search_string = request.get('search_string', '')
        if search_string:
            search_string = '* OR '.join(search_string.split())+'*'

        all_groups = [i.getObject() for i in self.portal_catalog(
                             {'portal_type':'Group',
                              'path':'/'.join(self.context.getPhysicalPath()),
                              'SearchableText':search_string,
                               'sort_on':'sortable_title'
                              })]

        return all_groups

    def search_persons_in_group(self, request, search_string, group_id):
        """
        This method will be used to search for persons inside groups.
        """

        # I'm modifying the search string so the search is able to return
        # a result, even if no full word is provided
        search_string = request.get('search_string', '')
        if search_string:
            search_string = '* OR '.join(search_string.split())+'*'

        all_persons = [i.getObject() for i in self.portal_catalog(
                             {'portal_type':'Person',
                              'path':'/'.join(self.context.getPhysicalPath()),
                              'SearchableText':search_string,
                               'sort_on':'id'
                              })]
                              
        group = getattr(self.context, group_id, None)
        if not group:
            return []
        
        persons_in_group = group.persons
        
        results = []

        # Now i filter the results
        for person in all_persons:
            if person in group.persons and person not in results:
                results.append(person)
                    
        return results

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
