# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.contacts import contactsMessageFactory as _

class IPerson(Interface):
    """Contact information of a person"""

    # -*- schema definition goes here -*-

    short_name = schema.TextLine(
        title=_(u"Short Name"),
        required=False,
        description=_(u"Person's short name"),
    )
    first_name = schema.TextLine(
        title=_(u"First Name"), 
        required=True,
        description=_(u"Person's first name"),
    )
    last_name = schema.TextLine(
        title=_(u"Last Name"), 
        required=True,
        description=_(u"Person's last name"),
    )
    organization = schema.Object(
        title=_(u"Organization"),
        required=False,
        description=_(u"The organization the person belongs to"),
        schema=Interface, # specify the interface(s) of the addable types here
    )
    position = schema.TextLine(
        title=_(u"Position"),
        required=False,
        description=_(u"Person's position in the company"),
    )
    department= schema.TextLine(
        title=_(u"Department"),
        required=False,
        description=_(u"Department where this person works"),
    )
    work_phone = schema.TextLine(
        title=_(u"Work Phone Number"),
        required=False,
        description=_(u"Person's work phone number"),

    )
    work_mobile_phone = schema.TextLine(
        title=_(u"Work Mobile Phone Number"),
        required=False,
        description=_(u"Person's work mobile phone number"),
    )
    work_email = schema.TextLine(
        title=_(u"Work E-mail address"),
        required=False,
        description=_(u"Person's work e-mail address"),
    )
    work_email2 = schema.TextLine(
        title=_(u"2nd Work E-mail address (optional)"),
        required=False,
        description=_(u"A second work e-mail address"),
    )
    work_email3 = schema.TextLine(
        title=_(u"3nd Work E-mail address (optional)"),
        required=False,
        description=_(u"A third work e-mail address"),
    )
    photo = schema.Bytes(
        title=_(u"Photo"),
        required=False,
        description=_(u"Person's photo"),
    )
    address = schema.TextLine(
        title=_(u"Address"), 
        required=False,
        description=_(u"Person's address"),
    )
    country = schema.Choice(
        title=_(u"Country"),
        required=False,
        description=_(u"Person's country"),
        vocabulary='contacts.countries'
    )
    state = schema.Choice(
        title=_(u"State"),
        required=False,
        description=_(u"Person's state"),
        vocabulary='contacts.states'
    )
    city = schema.TextLine(
        title=_(u"City"),
        required=False,
        description=_(u"Person's city"),
    )
    phone = schema.TextLine(
        title=_(u"Phone Number"),
        required=False,
        description=_(u"Person's phone number"),
    )
    mobile_phone = schema.TextLine(
        title=_(u"Mobile Phone Number"),
        required=False,
        description=_(u"Person's mobile phone number"),
    )
    email = schema.TextLine(
        title=_(u"E-mail address"),
        required=False,
        description=_(u"Person's e-mail address"),
    )
    web = schema.TextLine(
        title=_(u"Web / Blog"),
        required=False,
        description=_(u"Person's web page or blog. Example: "
                       "http://www.google.com"),
    )
    text = schema.TextLine(
        title=_(u"Text"),
        required=False,
    )
