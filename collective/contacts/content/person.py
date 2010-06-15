# -*- coding: utf-8 -*-
"""Definition of the Person content type
"""

from Acquisition import aq_parent 
from AccessControl import ClassSecurityInfo
from zope.interface import implements, directlyProvides

from Products.CMFCore import permissions
from Products.CMFPlone.CatalogTool import sortable_title
from Products.CMFPlone.utils import safe_unicode
from Products.Archetypes import atapi
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget, registerField
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from plone.indexer import indexer

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IPerson
from collective.contacts.config import PROJECTNAME
from collective.contacts.content import DeprecatedATFieldProperty

class DateField(atapi.StringField):
    security  = ClassSecurityInfo()
    
    def _split(self, instance, **kwargs):
        try:
            value = self.getStorage(instance).get(self.getName(), instance, **kwargs).split('/')
            return value[0], value[1]
        except:
            return None, None

    security.declareProtected(permissions.View, 'getLocalized')
    def getLocalized(self, instance, **kwargs):
        month, day = self._split(instance)
        if not day or not month:
            return ''
        return _(u'date_format', default=u'${m}/${d}', mapping={'d': day,
                                                                'm': month})

    security.declareProtected(permissions.View, 'getDay')
    def getDay(self, instance, **kwargs):
        month, day = self._split(instance)
        return day and int(day) or day

    security.declareProtected(permissions.View, 'getMonth')
    def getMonth(self, instance, **kwargs):
        month, day = self._split(instance, **kwargs)
        return month and int(month) or month

class DateWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "date",
        })
    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """Basic impl for form processing in a widget"""
        fname = field.getName()
        month = form.get('%s_month' % fname, 0)
        day = form.get('%s_day' % fname, 0)
        if month and day:
            value = '%02d/%02d' % (int(month), int(day))
        else:
            value = ''
        if emptyReturnsMarker and value == '':
            return empty_marker
        # stick it back in request.form
        form[fname] = value
        return value, {}
    
@indexer(IPerson)
def organization(obj):
    return obj.organization.UID()
    
@indexer(IPerson)
def sortable_organization(obj):
    return sortable_title(organization)

@indexer(IPerson)
def birthdate(obj):
    field = obj.getField('birthdate')
    month, day = field.getMonth(obj), field.getMonth(obj)
    if not month or not day:
        return '0000'
    return '%02d%02d' % (month, day)

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

    DateField(
        'birthdate',
        storage=atapi.AnnotationStorage(),
        widget=DateWidget(
            label=_(u"Date of birth"),
            description=_(u"Person's date of birth"),
        ),
        required=False,
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
        'workPhoneInternal',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Internal Work Phone Number"),
            description=_(u"Person's internal work phone number"),
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
        'workFax',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Work Fax number"),
            description=_(u"Person's work fax number"),
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
        'zip',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ZIP"),
            description=_(u"Person's ZIP"),
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
    shortName = atapi.ATFieldProperty('shortName')
    lastName = atapi.ATFieldProperty('lastName')
    firstName = atapi.ATFieldProperty('firstName')
    birthdate = atapi.ATFieldProperty('birthdate')
    organization = atapi.ATReferenceFieldProperty('organization')
    position = atapi.ATFieldProperty('position')
    department = atapi.ATFieldProperty('department')
    workPhone = atapi.ATFieldProperty('workPhone')
    workPhoneInternal = atapi.ATFieldProperty('workPhoneInternal')
    workMobilePhone = atapi.ATFieldProperty('workMobilePhone')
    workFax = atapi.ATFieldProperty('workFax')
    workEmail = atapi.ATFieldProperty('workEmail')
    workEmail2 = atapi.ATFieldProperty('workEmail2')
    workEmail3 = atapi.ATFieldProperty('workEmail3')
    photo = atapi.ATFieldProperty('photo')
    address = atapi.ATFieldProperty('address')
    country = atapi.ATFieldProperty('country')
    state = atapi.ATFieldProperty('state')
    city = atapi.ATFieldProperty('city')
    zip = atapi.ATFieldProperty('zip')
    phone = atapi.ATFieldProperty('phone')
    mobilePhone = atapi.ATFieldProperty('mobilePhone')
    email = atapi.ATFieldProperty('email')
    web = atapi.ATFieldProperty('web')
    text = atapi.ATFieldProperty('text')
    
    # deprecated properties
    short_name = DeprecatedATFieldProperty('shortName', 'short_name')
    last_name = DeprecatedATFieldProperty('lastName', 'last_name')
    first_name = DeprecatedATFieldProperty('firstName', 'first_name')
    work_phone = DeprecatedATFieldProperty('workPhone', 'work_phone')
    work_mobile_phone = DeprecatedATFieldProperty('workMobilePhone', 'work_mobile_phone')
    work_email = DeprecatedATFieldProperty('workEmail', 'work_email')
    work_email2 = DeprecatedATFieldProperty('workEmail2', 'work_email2')
    work_email3 = DeprecatedATFieldProperty('workEmail3', 'work_email3')
    mobile_phone = DeprecatedATFieldProperty('mobilePhone', 'mobile_phone')
    
    def _compute_title(self):
        """Compute title from last and first name"""
        return safe_unicode('%s, %s' % (self.lastName, self.firstName))

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

registerField(DateField,
              title='Date',
              description='Used for storing dates without years')

registerWidget(DateWidget,
               title='Date',
               description=('Renders a day and a month drop down'),
               used_for=('collective.contacts.content.person.DateField',)
               )
