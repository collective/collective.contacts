import unittest

from collective.contacts.tests.integration.person import TestPerson

def test_suite():
    """Test suit"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPerson))
    return suite