"""Definition of the Address Book content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IAddressBook
from collective.contacts.config import PROJECTNAME

AddressBookSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

AddressBookSchema['title'].storage = atapi.AnnotationStorage()
AddressBookSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    AddressBookSchema,
    folderish=True,
    moveDiscussion=False
)

class AddressBook(folder.ATFolder):
    """An address book"""
    implements(IAddressBook)

    portal_type = "Address Book"
    schema = AddressBookSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(AddressBook, PROJECTNAME)
