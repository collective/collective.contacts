# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from collective.contacts import contactsMessageFactory as _

class IAddressBook(Interface):
    """An address book"""
    sectors = schema.TextLine(
        title=_(u"Sectors"),
        required=False,
        description=_(u"Add here sectors and subsectors that will be used by "
                       "organizations."),
    )
    # -*- schema definition goes here -*-
