from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from collective.contacts import contactsMessageFactory as _

class IAddressBook(Interface):
    """An address book"""
    
    # -*- schema definition goes here -*-
