# -*- coding: utf-8 -*-
"""Integration tests suit"""
import unittest

from collective.contacts.tests.integration.person import TestPerson
from collective.contacts.tests.integration.addressbook import TestAddressBook
from collective.contacts.tests.integration.setup import TestSetup


def test_suite():
    """Test suit"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPerson))
    suite.addTest(unittest.makeSuite(TestAddressBook))
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite