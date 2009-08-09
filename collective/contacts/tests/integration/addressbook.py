# -*- coding: utf-8 -*-
"""Integration tests for the Address Book content type"""
from collective.contacts.tests.base import TestCase

class TestAddressBook(TestCase):

    def afterSetUp(self):
        self.test_sectors = [
            {'sector': 'uno', 'sub_sector':('uno_1', 'uno_2')},
            {'sector': 'dos', 'sub_sector':('dos_1', 'dos_2', 'dos_3')}
        ]

    def test_get_sectors(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Address Book', 'ab1')
        self.portal.ab1.setSectors(self.test_sectors)
        sectors = self.portal.ab1.get_sectors()
        self.assertEquals(sectors, ['uno', 'dos'])

    def test_get_sector_subsectors(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Address Book', 'ab1')
        self.portal.ab1.setSectors(self.test_sectors)
        sub_sectors = self.portal.ab1.get_sub_sectors('dos')
        self.assertEquals(sub_sectors, ['dos_1', 'dos_2', 'dos_3'])

    def test_get_all_subsectors(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Address Book', 'ab1')
        self.portal.ab1.setSectors(self.test_sectors)
        sub_sectors = self.portal.ab1.get_all_sub_sectors()
        self.assertEquals(
            sub_sectors,
            ['uno_1', 'uno_2','dos_1', 'dos_2', 'dos_3']
        )
