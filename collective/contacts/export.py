# -*- coding: utf-8 -*-
from StringIO import StringIO
from DateTime import DateTime
from DateTime.interfaces import DateError
from base64 import encodestring
import csv
import time
import re

from zope.i18n import translate
from zope.interface import implements
from zope.component import getUtility, getAdapter
from zope.schema.interfaces import IVocabularyFactory

from Products.ATContentTypes.lib.calendarsupport import rfc2445dt, n2rn, vformat
from Products.CMFPlone.utils import safe_callable

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import ISearch, IPerson, IOrganization, IExport

class AbstractCSVExport(object):
    """ Abstract CSV export
    
        Subclasses need to provide the following attributes:
        
        * name: the name of the corresponding CustomizableColumns
                adapter
        * fields: list of attributes to be included in the csv
    """
    title = "CSV"
    
    def __init__(self, context):
        self.context = context
    
    def export(self, request=None, objects=None):
        data = StringIO()
        writer = csv.writer(data)
    
        # I add them to the first row in the CSV
    
        writer.writerow(self.fields)
        
        # if no persons are given fetch all objects using the search adapter
        if objects is None:
            search = getAdapter(self.context, interface=ISearch, name=self.name)
            objects = search.search()
        
        # And now, for each person, i load his data on each column
    
        for object in objects:
            row = []
            for field in self.fields:
                # there's only one exception, if the field is organizations,
                # we need the organization's name, not the object
                if field == 'organization':
                    organization = getattr(object,field)
                    if organization:
                        row.append(organization.id)
                    else:
                        row.append('')
                else:
                    row.append(getattr(object,field))
    
            writer.writerow(row)
        
        if request:
            self._addResponseHeaders(request, data)
        return data.getvalue()
    
    def _addResponseHeaders(self, request, data):
        request.RESPONSE.setHeader('Content-Type','application/csv')
        request.RESPONSE.setHeader('Content-Length',len(data.getvalue()))
        request.RESPONSE.setHeader('Content-Disposition',
                                   'inline;filename=%s-%s.csv' %(
                                   self.name,
                                   time.strftime("%Y%m%d-%H%M%S",time.localtime())))
        
class PersonCSVExport(AbstractCSVExport):
    implements(IExport)
    name = "person"
    fields = ["id",
              "shortName",
              "firstName", 
              "lastName", 
              "birthdate",
              "organization", 
              "position", 
              "department", 
              "workPhone", 
              "workMobilePhone", 
              "workEmail", 
              "workEmail2", 
              "workEmail3", 
              "address", 
              "country",
              "state",
              "city",
              "zip",
              "phone", 
              "mobilePhone", 
              "email", 
              "web", 
              "text"]
        
class OrganizationCSVExport(AbstractCSVExport):
    implements(IExport)
    name = "organization"
    fields = ["id",
              "title",
              "address",
              "city",
              "zip",
              "country",
              "state",
              "extraAddress",
              "phone",
              "fax",
              "email",
              "email2",
              "email3",
              "web",
              "sector",
              "sub_sector",
              "text"]

class AbstractTemplateExport(object):
    global_template = "%s"
    template = """BEGIN:VCARD
VERSION:3.0
%(contents)s
END:VCARD
"""
    contents = ""
    noescape = ['web', 'revision', 'birthdate', 'photo']
    required = []
    
    def __init__(self, context):
        self.context = context
        self.countries = None
        self.states = None
        
    def organization(self, object, value):
        if value:
            return value.Title()
        return ''
    
    def revision(self, object, value):
        return rfc2445dt(DateTime(object.ModificationDate()))
    
    def birthdate(self, object, value):
        if value:
            field = object.getField('birthdate')
            return '0000-%02d-%02d' % (field.getMonth(object), field.getDay(object))
        return ''
    
    def country(self, object, value):
        if value:
            if not self.countries:
                self.countries = getUtility(IVocabularyFactory, name='contacts.countries')(self.context)
            try:
                return self.countries.getTerm(value).title.encode('utf-8')
            except:
                pass
        return ''
    
    def state(self, object, value):
        if value:
            if not self.states:
                self.states = getUtility(IVocabularyFactory, name='contacts.states')(self.context)
            try:
                return self.states.getTerm(value).title.encode('utf-8')
            except:
                pass
        return ''
    
    def photo(self, object, value):
        if value and value.get_size():
            data = encodestring(object.getField('photo').getScale(object, 'thumb').data)
            return 'PHOTO;ENCODING=BASE64;TYPE=%s:\n  %s' % (value.getContentType()[6:].upper(), data.strip().replace('\n', '\n  '))
        return ''

    def getEntry(self, object):
        lines = []
        attrs = re.findall('%\([^\)]+\)', self.contents)
        map = {}
        for attr in attrs:
            attr = attr[2:-1]
            if map.has_key(attr):
                continue
            value = getattr(object, attr, '')
            modifier = getattr(self, attr, None)
            if modifier and safe_callable(modifier):
                value = modifier(object, value)
            elif safe_callable(value):
                value = value()
            if value and not attr in self.noescape:
                value = vformat(value)
            map[attr] = value
        for required in self.required:
            if not map[required]:
                return ''
        return self.template % {'contents': self.contents % map}
    
    def _addResponseHeaders(self, request, data, name):
        request.RESPONSE.setHeader('Content-Type','text/x-vcard; charset=utf-8')
        request.RESPONSE.setHeader('Content-Length',len(data.getvalue()))
        request.RESPONSE.setHeader('Content-Disposition',
                                   'inline;filename=%s-%s.vcf' %(
                                   name,
                                   time.strftime("%Y%m%d-%H%M%S",time.localtime())))
    
    def _export(self, objects, name, request=None):
        data = StringIO()
        for object in objects:
            data.write(self.getEntry(object))
        if request:
            self._addResponseHeaders(request, data, name)
        return self.global_template % data.getvalue()

class PersonVCardExport(AbstractTemplateExport):
    implements(IExport)
    title = _(u"Business Card (vCard)")
    
    contents = """N:%(lastName)s;%(firstName)s
FN:%(title)s
NICKNAME:%(shortName)s
ORG:%(organization)s
TITLE:%(position)s
ROLE:%(department)s
BDAY:%(birthdate)s
TEL;TYPE=WORK:%(workPhone)s
TEL;TYPE=WORK,CELL,MSG:%(workMobilePhone)s
EMAIL;TYPE=WORK,PREF:%(workEmail)s
EMAIL;TYPE=WORK:%(workEmail2)s
EMAIL;TYPE=WORK:%(workEmail3)s
TEL;TYPE=HOME:%(phone)s
TEL;TYPE=HOME,CELL,MSG:%(mobilePhone)s
EMAIL;TYPE=HOME,PREF:%(email)s
ADR;TYPE=HOME:;;%(address)s;%(city)s;%(state)s;%(zip)s;%(country)s
LABEL;TYPE=HOME:%(address)s\\n%(city)s, %(state)s %(zip)s\\n%(country)s
%(photo)s
URL:%(web)s
NOTE:%(text)s
UID:%(UID)s
REV:%(revision)s"""
        
    def export(self, request=None, objects=None):
        if not objects:
            if IPerson.providedBy(self.context):
                objects = [self.context]
            else:
                search = getAdapter(self.context, interface=ISearch, name='person')
                objects = search.search()
        return self._export(objects, len(objects)>1 and 'persons' or objects[0].getId(), request)

class OrganizationVCardExport(AbstractTemplateExport):
    implements(IExport)
    title = _(u"Business Card (vCard)")
    
    contents = """N:%(title)s
FN:%(title)s
TITLE:%(sector)s
ROLE:%(sub_sector)s
TEL;TYPE=WORK:%(phone)s
TEL;TYPE=WORK,FAX:%(workMobilePhone)s
EMAIL;TYPE=WORK,PREF,INTERNET:%(email)s
EMAIL;TYPE=WORK,INTERNET:%(email2)s
EMAIL;TYPE=WORK,INTERNET:%(email3)s
ADR;TYPE=WORK:;;%(address)s;%(extraAddress)s;%(city)s;%(state)s;%(zip)s;%(country)s
LABEL;TYPE=WORK:%(address)s\\n%(extraAddress)s\\n%(city)s, %(state)s %(zip)s\\n%(country)s
URL:%(web)s
NOTE:%(text)s
UID:%(UID)s
REV:%(revision)s"""
        
    def export(self, request=None, objects=None):
        if not objects:
            if IOrganization.providedBy(self.context):
                objects = [self.context]
            else:
                search = getAdapter(self.context, interface=ISearch, name='organization')
                objects = search.search()
        return self._export(objects, len(objects)>1 and 'organizations' or objects[0].getId(), request)

class PersonVCalendarExport(AbstractTemplateExport):
    implements(IExport)
    title = _(u"Birthday (vCal)")
    
    global_template = """BEGIN:VCALENDAR
VERSION:2.0
%s
END:VCALENDAR
"""
    template = """BEGIN:VEVENT
%(contents)s
END:VEVENT
"""
    contents = """UID:%(UID)s
DTSTAMP:%(revision)s
ORGANIZER;CN=%(title)s:MAILTO:%(email)s
DTSTART:%(birthday)s
DTEND:%(birthday)s
RRULE:FREQ=YEARLY;COUNT=0
SUMMARY:%(birthdaysummary)s"""
    required = ['birthday',]
    
    def __init__(self, context):
        self.context = context
        self.noescape += ['birthdate',]
        
    def birthday(self, object, value):
        field = object.getField('birthdate')
        now = DateTime()
        month, day = field.getMonth(object), field.getDay(object)
        try:
            return '%s%02d%02d' % (now.year(), int(month), int(day))
        except:
            pass
        return ''
    
    def birthdaysummary(self, object, value):
        name = object.title.decode('utf-8')
        if hasattr(self.context, 'REQUEST'):
            return translate(_(u'Birthday of ${name}', mapping={'name': name}), context=self.context.REQUEST).encode('utf-8')
        return ('Birthday of %s' % name.decode('utf-8')).encode('utf-8')
        
    def export(self, request=None, objects=None):
        if not objects:
            if IPerson.providedBy(self.context):
                objects = [self.context]
            else:
                search = getAdapter(self.context, interface=ISearch, name='person')
                objects = search.search()
        return self._export(objects, len(objects)>1 and 'persons' or objects[0].getId(), request)
    
    def _addResponseHeaders(self, request, data, name):
        request.RESPONSE.setHeader('Content-Type','text/calendar')
        request.RESPONSE.setHeader('Content-Length',len(data.getvalue()))
        request.RESPONSE.setHeader('Content-Disposition',
                                   'inline;filename=%s-%s.ics' %(
                                   name,
                                   time.strftime("%Y%m%d-%H%M%S",time.localtime())))
    