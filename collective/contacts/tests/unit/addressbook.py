"""Unit test module for the Address Book content type
"""

from plone.mocktestcase import MockTestCase
from mocker import KWARGS

import zope.component

from Products.Archetypes.interfaces import ISchema, IBaseObject
from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.ATContentTypes.content.base import ATCTContent

from collective.contacts.content.addressbook import AddressBook
from collective.contacts.interfaces import IAddressBook

class TestAddressBook(MockTestCase):
    """Test the Person type"""

    def setUp(self):
        zope.component.provideAdapter(instanceSchemaFactory)
        # This line also does the trick (I don't know what is better):
        # self.mock_adapter(instanceSchemaFactory, ISchema, (IBaseObject,))

        self.fields = ['sectors',]

