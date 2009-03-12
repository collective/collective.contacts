"""Definition of the Address Book content type
"""

from AccessControl import ClassSecurityInfo

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions.ateapi import *

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IAddressBook
from collective.contacts.config import PROJECTNAME

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
AddressBookSchema['sectors'].subfield_types = {'sector':'string', 'sub_sector':'lines'}
AddressBookSchema['sectors'].subfield_vocabularies = {}
AddressBookSchema['sectors'].subfield_labels = {'sector':_('Sector'), 'sub_sector':_('Sub sector')}
#AddressBookSchema['sectors'].required_subfields = ('sector', 'sub_sector')
#AddressBookSchema['sectors'].subfield_validators = {'source':('is_source_name',), 'kinds':('is_not_empty_kinds',)}
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

    security.declarePublic('get_sectors')
    def get_sectors(self):
        """
        Get the sectors for the vocabulary
        """
        return [(i.get('sector'),i.get('sector')) for i in self.sectors]

    security.declarePublic('get_sub_sectors')
    def get_sub_sectors(self, sector):
        """
        Method used to get the sub sectors given a sector.
        """
        sub_sectors = []
        for i in self.sectors:
            if i.get('sector') == sector:
                # I need to check if the sector has subsectors, it can be a
                # scenario where there is a sector, but no sub-sectors
                if i.get('sub_sector'):
                    for j in i.get('sub_sector'):
                        to_add = (j,j)
                        if to_add not in sub_sectors:
                            sub_sectors.append((j,j))

        return sub_sectors

    security.declarePublic('get__all_sub_sectors')
    def get_all_sub_sectors(self):
        """
        We use this method as a starting point to the field's vocabulary.
        Showing every entry in the sub sectors.
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
