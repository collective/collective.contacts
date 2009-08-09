# -*- coding: utf-8 -*-
"""Unit test module for the Person content type"""

from plone.mocktestcase import MockTestCase

import zope.component

from Products.Archetypes.interfaces import ISchema, IBaseObject
from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.ATContentTypes.content.base import ATCTContent

from collective.contacts.content.person import Person
from collective.contacts.interfaces.person import IPerson

class TestPerson(MockTestCase):
    """Test the Person type"""

    def setUp(self):
        zope.component.provideAdapter(instanceSchemaFactory)
        # This line also does the trick (I don't know what is better):
        # self.mock_adapter(instanceSchemaFactory, ISchema, (IBaseObject,))

        self.fields = ['shortName',
                       'firstName',
                       'lastName',
                       'organization',
                       'position',
                       'department',
                       'workPhone',
                       'workMobilePhone',
                       'workEmail',
                       'workEmail2',
                       'workEmail3',
                       'photo',
                       'address',
                       'country',
                       'state',
                       'city',
                       'phone',
                       'mobilePhone',
                       'email',
                       'web',
                       'text'
                      ]

    def test_provides_interface(self):
        person = Person('foo')
        self.assertTrue(IPerson.providedBy(person))

    def test_schema_fields(self):
        person = Person('foo')
        for f in self.fields:
            self.assertTrue(f in [i.getName() for i in person.schema.fields()],
                            "The field '%s' is not in the schema" % (f,))

    def test_schema_fields_cardinal(self):
        # If you add a new field and don't update tests, this is the
        # test you will brake. :-)
        atct = ATCTContent('foo')
        person = Person('bar')
        self.assertEquals(len(atct.schema.fields()) + len(self.fields),
                          len(person.schema.fields()))

    def test_compute_title(self):
        person = Person('jsmith')
        person.last_name = 'Smith'
        person.first_name = 'Joe'
        self.assertEquals(person._compute_title(), 'Smith, Joe')

    def test_title_label(self):
        label = Person.schema['title'].widget.label
        self.assertEquals(label, 'Full Name')

    def test_title_is_computed(self):
        field = Person.schema['title']
        self.assertEquals(field.getType(),
                          'Products.Archetypes.Field.ComputedField')

    def test_description_is_hidden(self):
        visible = Person.schema['description'].widget.visible
        self.assertEquals(visible['view'], 'invisible')
        self.assertEquals(visible['edit'], 'invisible')
