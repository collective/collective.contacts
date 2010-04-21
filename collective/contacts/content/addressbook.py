# -*- coding: utf-8 -*-
"""Definition of the Address Book content type"""

from AccessControl import ClassSecurityInfo

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions.ateapi import *

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IAddressBook
from collective.contacts.config import PROJECTNAME

from Products.Archetypes.interfaces import IObjectInitializedEvent, IObjectEditedEvent
from zope.component import adapter
import transaction

AddressBookSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    RecordsField(
        name='sectors',
        widget=RecordsWidget(
            description=_('Add here sectors and subsectors that will be used '
                          'by organizations.'),
            visible={'view': 'invisible', 'edit': 'visible'},
            label=_('Sectors'),
        ),
        required=False,
    ),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

AddressBookSchema['title'].storage = atapi.AnnotationStorage()
AddressBookSchema['description'].storage = atapi.AnnotationStorage()

AddressBookSchema['sectors'].subfields = ('sector', 'sub_sector')
AddressBookSchema['sectors'].subfield_types = {
    'sector': 'string',
    'sub_sector': 'lines'
}
AddressBookSchema['sectors'].subfield_vocabularies = {}
AddressBookSchema['sectors'].subfield_labels = {
    'sector': _('Sector'),
    'sub_sector': _('Sub sector')
}
#AddressBookSchema['sectors'].required_subfields = ('sector', 'sub_sector')
#AddressBookSchema['sectors'].subfield_validators = {
#    'source': ('is_source_name',),
#    'kinds':('is_not_empty_kinds',)
#}
AddressBookSchema['sectors'].innerJoin = ', '
AddressBookSchema['sectors'].outerJoin = '<br />'
#AddressBookSchema['sectors'].widget.macro = 'dct_records_widget'

schemata.finalizeATCTSchema(
    AddressBookSchema,
    folderish=True,
    moveDiscussion=False
)

class AddressBook(folder.ATFolder):
    """An address book"""
    implements(IAddressBook)
    security = ClassSecurityInfo()

    portal_type = "Address Book"
    schema = AddressBookSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # Here i will list the fields that should be shown by default in
    # the table view for organizations
    show_on_organizations_view = [('title', True),
                                  ('sector', True),
                                  ('sub_sector', True),
                                  ('phone', True),
                                  ('fax', True),
                                  ('email', True),
                                  ('web', True),
                                  ('address', True),
                                  ('city', True),
                                  ('country', True),
                                  ('state', False),
                                  ('zip', False),
                                  ('extraAddress', False),
                                  ('email2', False),
                                  ('email3', False),
                                  ('text', False)]

    show_on_persons_view = [('title', True),
                            ('shortName', False),
                            ('firstName', False),
                            ('lastName', False),
                            ('organization', True),
                            ('position', False),
                            ('department', False),
                            ('workPhone', False),
                            ('workMobilePhone', False),
                            ('workEmail', False),
                            ('phone', True),
                            ('mobilePhone', True),
                            ('email', True),
                            ('web', True),
                            ('address', True),
                            ('city', True),
                            ('country', True),
                            ('state', False),
                            ('workEmail2', False),
                            ('workEmail3', False),
                            ('photo', False),
                            ('text', False)]


    security.declarePublic('get_sectors')
    def get_sectors(self):
        """Get the sectors"""
        return [i.get('sector') for i in self.sectors]

    security.declarePublic('get_sub_sectors')
    def get_sub_sectors(self, sector):
        """Get the sub sectors given a sector"""

        sub_sectors = []
        for i in self.sectors:
            if i.get('sector') == sector:
                # I need to check if the sector has subsectors, it can be a
                # scenario where there is a sector, but no sub-sectors
                if i.get('sub_sector'):
                    for j in i.get('sub_sector'):
                        to_add = (j,j)
                        if to_add not in sub_sectors:
                            sub_sectors.append(j)

        return sub_sectors

    security.declarePublic('get_all_sub_sectors')
    def get_all_sub_sectors(self):
        """We use this method as a starting point to the field's
        vocabulary. Showing every entry in the sub sectors.
        """
        sub_sectors = []
        for i in self.sectors:
            results = self.get_sub_sectors(i.get('sector'))
            for to_add in results:
                if to_add not in sub_sectors:
                    sub_sectors.append(to_add)

        return sub_sectors
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(AddressBook, PROJECTNAME)

def removeDups(obj):
    sectors = []
    result = []
    for i in obj.getSectors():
        if i['sector'] not in sectors:
            sectors.append(i['sector'])
            dic = {'sector': i['sector']}
            if 'sub_sector' in i:
                dic['sub_sector'] = [x for x in set(i['sub_sector'])]
                
            result.append(dic)

    return result

@adapter(IAddressBook, IObjectInitializedEvent)
def handle_addressbook_added(obj, event):
    """Handle the IObjectInitializedEvent event for an addressbook"""
    if not obj.REQUEST.get('form.button.more'):
        result = removeDups(obj)
        obj.setSectors(result)
        transaction.commit()


@adapter(IAddressBook, IObjectEditedEvent)
def handle_addressbook_edited(obj, event):
    """Handle the IObjectEditedEvent event for an addressbook"""
    if not obj.REQUEST.get('form.button.more'):
        result = removeDups(obj)
        obj.setSectors(result)
        transaction.commit()
