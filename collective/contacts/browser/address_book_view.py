from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.interfaces import IAddressBookView

import json

class AddressBookView(BrowserView):
    implements(IAddressBookView)

    pt = ViewPageTemplateFile('templates/address_book.pt')

    def get_categories(self, type='', contact_obj_path = ''):
        catalog = getToolByName(self.context, 'portal_catalog')
        if contact_obj_path:
            folder_path = contact_obj_path
        else:
            folder_path = '/'.join(self.context.getPhysicalPath())
        results = catalog(path={'query': folder_path}, portal_type=type)

        results_unique_objs = {}
        for x in results:
            results_unique_objs[x.UID] = x

        parsed_results = []
        if results_unique_objs.values():
            for categorie in results_unique_objs.values():
                obj_title = categorie.Title
                obj_url = categorie.getURL()
                obj_UID = categorie.UID
                parsed_results.append({'obj_title':obj_title,
                                     'obj_url':obj_url, 'UID': obj_UID})
        return parsed_results

    def get_persons(self,UID, search=''):
        result = []
        if UID:
            ref_catalog = getToolByName(self.context, 'reference_catalog')
            persons = []
            persons = ref_catalog.getBackReferences(UID)
            if not persons:
                group = ref_catalog.getReferences(UID)
                if group:
                    persons = group[0].persons
            result = self._parsePersons(persons,search)

        else:
            if search:
                catalog = getToolByName(self.context, 'portal_catalog')
                folder_path = '/'.join(self.context.getPhysicalPath())
                persons = catalog(path={'query': folder_path},
                                        portal_type='Person',
                                        Title='*%s*' % search)
                result = self._parsePersons(persons, from_catalog=True)
            else:
                result = self.get_categories(type="Person")
        return result

    def member_listing_view(self, UID ='', search=''):
        self.members_list = self.get_persons(UID, search)
        self.members_listing_template = ViewPageTemplateFile(
                                'templates/member_listing_template.pt')

        return self.members_listing_template(self)

    def member_data_view(self, memberUID =''):
        if memberUID:
            ref_catalog = getToolByName(self.context,
                                        'reference_catalog')
            self.person = ref_catalog._objectByUUID(memberUID)
            self.custom_context = self.context
            if memberUID:
                self.custom_context = \
                    self.context.reference_catalog.lookupObject(memberUID)
        self.members_data_template = ViewPageTemplateFile(
                                    'templates/member_data_template.pt')
        return self.members_data_template(self)

    def _parsePersons(self, persons, search="", from_catalog=False ):
        result = []
        if not search:
            if from_catalog:
                result = [{'obj_title':person.Title,
                           'obj_url':person.getURL(),
                           'UID':person.UID} for person in persons]
            else:
                result = [{'obj_title':person.Title(),
                           'obj_url':person._getURL(),
                           'UID':person.UID()} for person in persons]
        else:
            result = [{'obj_title':person.Title(),
                       'obj_url':person._getURL(),
                       'UID':person.UID()} for person in persons
                        if search.lower() in person.Title().lower()]
        return result
