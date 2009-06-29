# -*- coding: utf-8 -*-
"""Definition of the Person content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IPerson
from collective.contacts.config import PROJECTNAME

PersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ComputedField(
        'title',
        searchable=1,
        expression='context._compute_title()',
        accessor='Title'
    ),

    atapi.StringField(
        name='shortName',
        storage = atapi.AnnotationStorage(),
        required=False,
        searchable=1,
        #default='',
        #schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Short Name"),
            description=_(u"Person's short name"),
        ),
    ),

    atapi.StringField(
        'firstName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"First Name"),
            description=_(u"Person's first name"),
        ),
        searchable=1,
        required=True,
    ),

    atapi.StringField(
        'lastName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Last Name"),
            description=_(u"Person's last name"),
        ),
        searchable=1,
        required=True,
    ),

    atapi.ReferenceField(
        'organization',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Organization"),
            description=_(u"The organization the person belongs to"),
            allow_browse = True,
            restrict_browsing_to_startup_directory=True,
        ),
        searchable=1,
        relationship='person_organization',
        allowed_types=('Organization',),
        multiValued=False,
        required=False,
        schemata='work',
    ),

    atapi.StringField(
        'position',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Position"),
            description=_(u"Person's position in the company"),
        ),
        searchable=1,
        required=False,
        schemata='work',
    ),

    atapi.StringField(
        'department',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Department"),
            description=_(u"Department where this person works"),
        ),
        searchable=1,
        required=False,
        schemata='work',
    ),

    atapi.StringField(
        'workPhone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Work Phone Number"),
            description=_(u"Person's work phone number"),
        ),
        searchable=1,
        required=False,
        schemata='work',
    ),

    atapi.StringField(
        'workMobilePhone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Work Mobile Phone Number"),
            description=_(u"Person's work mobile phone number"),
        ),
        searchable=1,
        required=False,
        schemata='work',
    ),

    atapi.StringField(
        'workEmail',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Work E-mail address"),
            description=_(u"Person's work e-mail address"),
        ),
        validators=('isEmail',),
        required=False,
        schemata='work',
        searchable=1,
    ),

    atapi.StringField(
        'workEmail2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"2nd Work E-mail address (optional)"),
            description=_(u"A second work e-mail address"),
        ),
        validators=('isEmail',),
        required=False,
        schemata='work',
        searchable=1,
    ),

    atapi.StringField(
        'workEmail3',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"3rd Work E-mail address (optional)"),
            description=_(u"A third work e-mail address"),
        ),
        validators=('isEmail',),
        searchable=1,
        required=False,
        schemata='work',
    ),

    atapi.ImageField(
        'photo',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Photo"),
            description=_(u"Person's photo"),
        ),
        validators=('isNonEmptyFile',),
        required=False,
        sizes={'large' : (768, 768), 'preview' : (400, 400), 'mini' : (200, 200), 'thumb' : (128, 128), 'tile' : (64, 64), 'icon' : (32, 32), 'listing' : (16, 16)},
    ),

    atapi.StringField(
        'address',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Address"),
            description=_(u"Person's address"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'country',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_("Country"),
            description=_("Select a country")
        ),
        vocabulary_factory='contacts.countries',
        required=False,
        searchable=1
    ),

    atapi.StringField(
        'state',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"State"),
            description=_(u"Person's state"),
        ),
        vocabulary_factory='contacts.states',
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'city',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"City"),
            description=_(u"Person's city"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Phone Number"),
            description=_(u"Person's phone number"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'mobilePhone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Mobile Phone Number"),
            description=_(u"Person's mobile phone number"),
        ),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"E-mail address"),
            description=_(u"Person's e-mail address"),
        ),
        validators=('isEmail',),
        required=False,
        searchable=1,
    ),

    atapi.StringField(
        'web',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Web / Blog"),
            description=_(u"Person's web page or blog. Example: "
                           "http://www.google.com"),
        ),
        validators=('isURL',),
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
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

PersonSchema['title'].storage = atapi.AnnotationStorage()
PersonSchema["title"].widget.label = _('Full Name')
PersonSchema['description'].storage = atapi.AnnotationStorage()
PersonSchema['description'].widget.visible = {'edit': 'invisible',
                                              'view': 'invisible'}

PersonSchema['effectiveDate'].schemata = 'settings'
PersonSchema['expirationDate'].schemata = 'settings'
PersonSchema['creation_date'].schemata = 'settings'
PersonSchema['modification_date'].schemata = 'settings'

schemata.finalizeATCTSchema(PersonSchema, moveDiscussion=False)

class Person(base.ATCTContent):
    """Contact information of a person"""
    implements(IPerson)

    portal_type = 'Person'
    schema = PersonSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    short_name = atapi.ATFieldProperty('shortName')
    first_name = atapi.ATFieldProperty('firstName')
    last_name = atapi.ATFieldProperty('lastName')
    organization = atapi.ATReferenceFieldProperty('organization')
    position = atapi.ATFieldProperty('position')
    department = atapi.ATFieldProperty('department')
    work_phone = atapi.ATFieldProperty('workPhone')
    work_mobile_phone = atapi.ATFieldProperty('workMobilePhone')
    work_email = atapi.ATFieldProperty('workEmail')
    work_email2 = atapi.ATFieldProperty('workEmail2')
    work_email3 = atapi.ATFieldProperty('workEmail3')
    photo = atapi.ATFieldProperty('photo')
    address = atapi.ATFieldProperty('address')
    country = atapi.ATFieldProperty('country')
    state = atapi.ATFieldProperty('state')
    city = atapi.ATFieldProperty('city')
    phone = atapi.ATFieldProperty('phone')
    mobile_phone = atapi.ATFieldProperty('mobilePhone')
    email = atapi.ATFieldProperty('email')
    web = atapi.ATFieldProperty('web')
    text = atapi.ATFieldProperty('text')
    
    def _compute_title(self):
        """Compute title from last and first name"""
        return '%s, %s' % (self.last_name, self.first_name)

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('photo').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """
        Transparent access to image scales.
        Taken from http://www.unc.edu/~jj/plone/#imagefieldscales
        """
        if name.startswith('photo'):
            field = self.getField('photo')
            image = None
            if name == 'photo':
                image = field.getScale(self)
            else:
                scalename = name[len('photo_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return super(Person, self).__bobo_traverse__(REQUEST, name)


atapi.registerType(Person, PROJECTNAME)
