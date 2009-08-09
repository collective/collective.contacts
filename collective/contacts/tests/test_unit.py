# -*- coding: utf-8 -*-
"""Unit tests suit"""
import unittest

from collective.contacts.tests.unit.person import TestPerson
from collective.contacts.tests.unit.addressbook import TestAddressBook

def test_suite():
    """Test suit"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPerson))
    suite.addTest(unittest.makeSuite(TestAddressBook))
    return suite