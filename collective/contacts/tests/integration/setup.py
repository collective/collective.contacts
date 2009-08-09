# -*- coding: utf-8 -*-
"""Integration tests for the Address Book content type"""

from Products.CMFCore.utils import getToolByName

from collective.contacts.tests.base import TestCase

class TestSetup(TestCase):

    def afterSetUp(self):
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.types = getToolByName(self.portal, 'portal_types')
        self.quickinstaller = getToolByName(
            self.portal,
            'portal_quickinstaller'
        )

    def test_types_installed(self):
        """Test that content types are properly registerd"""
        addressbook_fti = getattr(self.types, 'Address Book')
        self.assertEquals('Address Book', addressbook_fti.title)

        group_fti = getattr(self.types, 'Group')
        self.assertEquals('Group', group_fti.title)

        person_fti = getattr(self.types, 'Person')
        self.assertEquals('Person', person_fti.title)

        organization_fti = getattr(self.types, 'Organization')
        self.assertEquals('Organization', organization_fti.title)

    def test_globally_allowed(self):
        """Test the globally allowed property for this products' types"""
        addressbook_fti = getattr(self.types, 'Address Book')
        self.failUnless(addressbook_fti.global_allow)

        group_fti = getattr(self.types, 'Group')
        self.failIf(group_fti.global_allow)

        person_fti = getattr(self.types, 'Person')
        self.failIf(person_fti.global_allow)

        organization_fti = getattr(self.types, 'Organization')
        self.failIf(organization_fti.global_allow)

    def test_addressbook_allowed_content_types(self):
        """Test allowed content types inside an Address Book"""
        fti = getattr(self.types, 'Address Book')
        self.failUnless('Person' in fti.allowed_content_types)
        self.failUnless('Organization' in fti.allowed_content_types)
        self.failUnless('Group' in fti.allowed_content_types)
        self.failIf(len(fti.allowed_content_types) != 3)

    def test_indexes_added(self):
        """Test that indexes are added at install time"""
        indexes = (('firstName', 'FieldIndex'),
                   ('lastName', 'FieldIndex'),
                  )
        indexes = dict(indexes).keys()

        for index in indexes:
            self.failUnless(self.catalog.Indexes.get(index, None) is not None)
