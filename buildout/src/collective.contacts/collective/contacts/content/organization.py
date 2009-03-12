"""Definition of the Organization content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IOrganization
from collective.contacts.config import PROJECTNAME

OrganizationSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'address',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Address"),
            description=_(u"Organization's address"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'city',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"City"),
            description=_(u"Organization's city"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'zip',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ZIP"),
            description=_(u"Organization's ZIP"),
        ),
        required=False,
        searchable=1,
    ),

    # Este campo deberia ser un drop down con todos los paises listados
    atapi.StringField(
        'country',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Country"),
            description=_(u"Organization's country"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'extraAddress',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Extra Address Info"),
            description=_(u"Organization's extra address information."),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Phone Number"),
            description=_(u"Organization's phone number"),
        ),
        searchable=1,
    ),

    atapi.StringField(
        'fax',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Fax number"),
            description=_(u"Organization's fax number"),
        ),
        searchable=1,
    ),

    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"E-mail address"),
            description=_(u"Organization's e-mail address"),
        ),
        validators=('isEmail'),
        required=True,
        searchable=1,
    ),

    atapi.StringField(
        'email2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"2nd E-mail address"),
            description=_(u"Organization's 2nd e-mail address"),
        ),
        validators=('isEmail'),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'email3',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"3rd E-mail address"),
            description=_(u"Organization's 3rd e-mail address"),
        ),
        validators=('isEmail'),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'web',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Web"),
            description=_(u"Organization's web page or blog"),
        ),
        required=False,
        searchable=1,
        validators=('isURL'),
    ),

    #ESto deberia ser un drop down con opciones de rubros
    atapi.StringField(
        'sector',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Sector"),
            description=_(u"Organization's sector"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Text"),
        ),
        required=False,
        searchable=1,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

OrganizationSchema['title'].storage = atapi.AnnotationStorage()
OrganizationSchema["title"].widget.label = _('Name')
OrganizationSchema['description'].storage = atapi.AnnotationStorage()
OrganizationSchema['description'].widget.visible = {'edit': 'invisible',
                                                    'view': 'invisible'}


schemata.finalizeATCTSchema(OrganizationSchema, moveDiscussion=False)

class Organization(base.ATCTContent):
    """Contact information of an organization"""
    implements(IOrganization)

    portal_type = "Organization"
    schema = OrganizationSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    address = atapi.ATFieldProperty('address')
    city = atapi.ATFieldProperty('city')
    zip = atapi.ATFieldProperty('zip')
    country = atapi.ATFieldProperty('country')
    extra_address = atapi.ATFieldProperty('extraAddress')
    phone = atapi.ATFieldProperty('phone')
    fax = atapi.ATFieldProperty('fax')
    email = atapi.ATFieldProperty('email')
    email2 = atapi.ATFieldProperty('email2')
    email3 = atapi.ATFieldProperty('email3')
    web = atapi.ATFieldProperty('web')
    sector = atapi.ATFieldProperty('sector')
    text = atapi.ATFieldProperty('text')


atapi.registerType(Organization, PROJECTNAME)