# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.contacts import contactsMessageFactory as _

class IOrganization(Interface):
    """Contact information of an organization"""

    # -*- schema definition goes here -*-
    title = schema.TextLine(
        title=_(u"Name"),
        required=False,
    )
    address = schema.TextLine(
        title=_(u"Address"),
        required=False,
    )
    country = schema.Choice(
        title=_(u"Country"),
        required=False,
        vocabulary='contacts.countries'
    )
    state = schema.Choice(
        title=_(u"State"),
        required=False,
        vocabulary='contacts.states'
    )
    city = schema.TextLine(
        title=_(u"City"),
        required=False,
    )
    zip = schema.TextLine(
        title=_(u"ZIP"),
        required=False,
    )
    extraAddress = schema.TextLine(
        title=_(u"Extra Address Info"),
        required=False,
    )
    phone = schema.TextLine(
        title=_(u"Phone Number"),
        required=False,
    )
    phoneInternal = schema.TextLine(
        title=_(u"Internal Phone Number"),
        required=False,
    )
    fax = schema.TextLine(
        title=_(u"Fax number"),
        required=False,
    )
    email = schema.TextLine(
        title=_(u"E-mail address"),
        required=False,
    )
    email2 = schema.TextLine(
        title=_(u"2nd E-mail address"),
        required=False,
    )
    email3 = schema.TextLine(
        title=_(u"3rd E-mail address"),
        required=False,
    )
    web = schema.TextLine(
        title=_(u"Web"),
        required=False,
    )
    sector = schema.Choice(
        title=_(u"Sector"),
        required=False,
        vocabulary='contacts.sectors',
    )
    sub_sector = schema.Choice(
        title=_(u"Sub sector"),
        required=False,
        vocabulary='contacts.sub_sectors',
    )
    text = schema.TextLine(
        title=_(u"Text"),
        required=False,
    )