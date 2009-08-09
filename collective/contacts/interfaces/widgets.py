# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import Iterable

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.contacts')

class ICountriesStates(Interface):
    countries = Iterable(
        title = _(u"countries"),
        description=_(u"A list of countries")
        )
    states = Iterable(
        title = _(u"states"),
        description=_(u"A list of states")
        )