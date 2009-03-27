from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from zope.app import zapi
from collective.contacts.interfaces import ICountriesStates
from collective.contacts.vocabularies import TitledVocabulary

class IOrganizationsSearchView(Interface):
    """
    OrganizationsSearch view interface
    """

    def allCountries():
        """
            Method that returns all countries from the vocabulary
        """

    def allStates():
        """
            Method that returns all states from the vocabulary
        """

    def test():
        """method that does the same as test on old page templates"""



class OrganizationsSearchView(BrowserView):
    """
    OrganizationsSearch browser view
    """
    implements(IOrganizationsSearchView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def allCountries(self):
        """
            Method that returns all countries from the vocabulary
        """
        utility = zapi.getUtility(ICountriesStates)
        results = TitledVocabulary.fromTitles(utility.countries)

        return results._terms

    def allStates(self):
        """
            Method that returns all states from the vocabulary
        """
        utility = zapi.getUtility(ICountriesStates)
        return utility.allStateValues()

    def test(self, condition, true_value, false_value):
        """
        method that does the same as test on old page templates
        """

        if condition:
            return true_value
        else:
            return false_value
