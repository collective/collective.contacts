"""
$Id: vocabularies.py 1957 2008-09-03 23:16:52Z javimansilla $

vocabularies for getpaid
"""

from zope.interface import implements, implementer, alsoProvides
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.component import _api as zapi
from os import path

from zope.schema import vocabulary

from iso3166 import CountriesStatesParser
from interfaces import ICountriesStates


from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.contacts')

class TitledVocabulary(vocabulary.SimpleVocabulary):
    def fromTitles(cls, items, *interfaces):
        """Construct a vocabulary from a list of (value,title) pairs.

        The order of the items is preserved as the order of the terms
        in the vocabulary.  Terms are created by calling the class
        method createTerm() with the pair (value, title).

        One or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        terms = [cls.createTerm(value,value,title) for (value,title) in items]
        return cls(terms, *interfaces)
    fromTitles = classmethod(fromTitles)

class CountriesStatesFromFile(object):
    """Countries utility that reads data from a file
    """
    implements(ICountriesStates)

    _no_values = [(u'(no values)',_(u'(no values)'))]
    # Be careful, somewhere else, there is code that asumes that state values
    # length is <= 6. Don't modify this ones that are part of the vocabulary
    _not_aplicable = [(u'??NA',_(u'Not Applicable'))]
    _allowed_no_values = [(u'??NV',_(u'(no values)'))]

    def __init__(self):
        iso3166_path = path.join(path.dirname(__file__), 'iso3166')
        self.csparser = CountriesStatesParser(iso3166_path)
        self.csparser.parse()
        self.loaded_countries = []

    def special_values(self):
        return [self._no_values[0],
                self._not_aplicable[0],
                self._allowed_no_values[0]]
    special_values = property(special_values)

    def countries(self):
        if self.loaded_countries:
            return self.loaded_countries
        names =  self.csparser.getCountriesNameOrdered()
        res = []
        for n in names:
            if len(n[1]) < 18:
                res.append( n )
            elif ',' in n:
                res.append( ( n[0], n[1].split(',')[0] ) )
            else:
                #This may show the countries wrongly abbreviated (in fact i am
                #almost sure it will, but is better than not showing them at all
                res.append( ( n[0], n[1][:18] ) )

        # need to pick this up some list of strings property in the admin interface
        def sorter( x, y, order=['ARGENTINA']):
            if x[1] in order and y[1] in order:
                return cmp( order.index(x[1]), order.index(y[1]) )
            if x[1] in order:
                return -1
            if y[1] in order:
                return 1
            return cmp( x[1], y[1] )

        res.sort( sorter )
        self.loaded_countries = res
        return res

    countries = property(countries)

    def states(self, country=None, allow_no_values=False):
        if country is None:
            states = self._not_aplicable + self.allStates()
        else:
            states = self.csparser.getStatesOf(country)

        if len(states) == 0:
            states = self._not_aplicable
        elif allow_no_values:
            states = self._allowed_no_values + states
        else:
            states = self._no_values + states
        return states

    def allStates(self):
        return self.csparser.getStatesOfAllCountries()

    def allStateValues(self):
        all_states = self.csparser.getStatesOfAllCountries()
        return self._allowed_no_values + self._not_aplicable + all_states

@implementer(IVocabulary)
def Countries( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.countries)
alsoProvides(Countries, IVocabularyFactory)

@implementer(IVocabulary)
def States( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.allStateValues())
alsoProvides(States, IVocabularyFactory)

@implementer(IVocabulary)
def Sectors( context ):
    address_book = context.aq_inner.aq_parent
    sectors = address_book.get_sectors()
    return TitledVocabulary.fromTitles(zip(sectors, sectors))
alsoProvides(Sectors, IVocabularyFactory)

@implementer(IVocabulary)
def SubSectors( context ):
    address_book = context.aq_inner.aq_parent
    sub_sectors = address_book.get_all_sub_sectors()
    return TitledVocabulary.fromTitles(zip(sub_sectors,sub_sectors))
alsoProvides(SubSectors, IVocabularyFactory)