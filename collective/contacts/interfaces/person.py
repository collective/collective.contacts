# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.contacts.interfaces import IOrganization
from collective.contacts import contactsMessageFactory as _

class IPerson(Interface):
    """Contact information of a person"""

    # -*- schema definition goes here -*-

    short_name = schema.TextLine(
        title=_(u"Short Name"),
        required=False,
    )
    first_name = schema.TextLine(
        title=_(u"First Name"), 
        required=True,
    )
    last_name = schema.TextLine(
        title=_(u"Last Name"), 
        required=True,
    )
    organization = schema.Object(
        title=_(u"Organization"),
        required=False,
        schema=IOrganization, # specify the interface(s) of the addable types here
    )
    position = schema.TextLine(
        title=_(u"Position"),
        required=False,
    )
    department= schema.TextLine(
        title=_(u"Department"),
        required=False,
    )
    work_phone = schema.TextLine(
        title=_(u"Work Phone Number"),
        required=False,
    )
    work_mobile_phone = schema.TextLine(
        title=_(u"Work Mobile Phone Number"),
        required=False,
    )
    work_email = schema.TextLine(
        title=_(u"Work E-mail address"),
        required=False,
    )
    work_email2 = schema.TextLine(
        title=_(u"2nd Work E-mail address (optional)"),
        required=False,
    )
    work_email3 = schema.TextLine(
        title=_(u"3nd Work E-mail address (optional)"),
        required=False,
    )
    photo = schema.Bytes(
        title=_(u"Photo"),
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
    phone = schema.TextLine(
        title=_(u"Phone Number"),
        required=False,
    )
    mobile_phone = schema.TextLine(
        title=_(u"Mobile Phone Number"),
        required=False,
    )
    email = schema.TextLine(
        title=_(u"E-mail address"),
        required=False,
    )
    web = schema.TextLine(
        title=_(u"Web / Blog"),
        required=False,
    )
    text = schema.TextLine(
        title=_(u"Text"),
        required=False,
    )
