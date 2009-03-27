# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, WARNING
from config import PROJECTNAME
import zope.i18n

from collective.contacts import contactsMessageFactory as _

import codecs
import csv

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

def strToInt(data):
    return int(data)

def strToFloat(data):
    return float(data)

def removeExtension(filename):
    if '.' in filename:
        filename = filename[:filename.rfind('.')]

    return filename


def importCSVPersons(context, path, file):
    """
    This function is used to import persons to a given path using a CSV file
    """
    aux = _('Starting the persons import process')
    msg = zope.i18n.translate(aux, context=context.request)

    LOG(PROJECTNAME, INFO, msg)

    portal_catalog = getToolByName(context, 'portal_catalog')

    # Now that we have all our configuration, we can start

    # First we set our results as an empty list, we will be loading
    # each user here
    results = []

    # we first make sure the content is in utf8
    reader = UnicodeReader(file)

    # Now we first load the headers
    headers = reader.next()
    rowLength = len(headers)
    counter = 0

    # Now i have to continue loading the rest of the persons
    for row in reader:
        # We now check that we have consistency in our CSV
        assert len(row) == rowLength
        result = {}
        for j in range(rowLength):
            result[headers[j]] = row[j]

        # And now, i have a new user, i add it to the results
        results.append(result)
        counter += 1

    aux = _('${persons_number} persons to be added to ${location}.',\
            mapping={'persons_number':counter,
                     'location':path})
    msg = zope.i18n.translate(aux, context=context.request)
    LOG(PROJECTNAME, INFO, msg)

    counter = 0

    # I now have all persons in my results, so i should start adding them to
    # the site
    for person in results:
        organization =[i.getObject() for i in portal_catalog(
                                    portal_type = 'Organization',
                                    path = path,
                                    Title = person['organization']
                                    )]


        if organization and len(organization)>1:
            aux = _('There are ${org_size} organizations with the same title, '
                    'i don\'t know with which one relate this person.',\
                    mapping={'org_size':len(organization)})

            msg = zope.i18n.translate(aux, context=context.request)
            LOG(PROJECTNAME, WARNING, msg)

            aux = _('You will have to load the person with id ${person_id} '
                    'manually.',\
                    mapping={'person_id':person['id']})
            msg = zope.i18n.translate(aux, context=context.request)
            LOG(PROJECTNAME, WARNING, msg)

        elif ((organization and len(organization)==1) or
             person['organization'] == ''):
            if context.get(person['id']):
                aux = _('There\'s already a person with this id here.')
                msg = zope.i18n.translate(aux, context=context.request)
                LOG(PROJECTNAME, WARNING, msg)

                aux = _('You will have to load the person with id '
                        '${person_id} manually.',\
                        mapping={'person_id':person['id']})
                msg = zope.i18n.translate(aux, context=context.request)
                LOG(PROJECTNAME, WARNING, msg)
                
            else:
                try:
                    context.invokeFactory('Person', person['id'])
                    new_person = context.get(person['id'])
                    for attr in person.keys():
                        if attr != 'id' and attr != 'organization':
                            setattr(new_person, attr, person[attr])
                        if (attr == 'organization' and
                            person['organization'] != ''):
                            new_person.setOrganization(organization[0])

                    counter += 1
                    portal_catalog.reindexObject(new_person)

                    aux = _('Successfuly added ${person_id}.',\
                            mapping={'person_id':person['id']})
                    msg = zope.i18n.translate(aux, context=context.request)
                    LOG(PROJECTNAME, INFO, msg)

                except:
                    aux = _('There was an error while adding.')
                    msg = zope.i18n.translate(aux, context=context.request)
                    LOG(PROJECTNAME, WARNING, msg)

                    aux = _('You will have to load the person with id '
                            '${person_id} manually.',\
                            mapping={'person_id':person['id']})
                    msg = zope.i18n.translate(aux, context=context.request)
                    LOG(PROJECTNAME, WARNING, msg)
        else:
            aux = _('There\'s no organization with title ${organization_name}, '
                    'make sure it exists before adding persons. '
                    '${person_id} not added',\
                    mapping={'organization_name':person['organization'],
                             'person_id':person['id']})
            msg = zope.i18n.translate(aux, context=context.request)
            LOG(PROJECTNAME, WARNING, msg)

    aux = _('Successfuly added ${persons_number} persons to ${location}.',\
            mapping={'persons_number':counter,
                     'location':path})
    msg = zope.i18n.translate(aux, context=context.request)
    LOG(PROJECTNAME, INFO, msg)

    return counter


def importCSVOrganizations(context, path, file):
    """
    This function is used to import organizations to a given path using
    a CSV file.
    """

    aux = _("Starting the organizations import process")
    msg = zope.i18n.translate(aux, context=context.request)
    LOG(PROJECTNAME, INFO, msg)
    # First we set our results as an empty list, we will be loading
    # each user here
    results = []

    portal_catalog = getToolByName(context, 'portal_catalog')

    # we first make sure the content is in utf8
    reader = UnicodeReader(file)

    # Now we first load the headers
    headers = reader.next()
    rowLength = len(headers)
    counter = 0

    # Now i have to continue loading the rest of the persons
    for row in reader:
        # We now check that we have consistency in our CSV
        assert len(row) == rowLength
        result = {}
        for j in range(rowLength):
            result[headers[j]] = row[j]

        # And now, i have a new user, i add it to the results
        results.append(result)
        counter += 1

    aux = _('${organizations_number} organizations to be added to ${location}.',\
            mapping={'organizations_number':counter,
                     'location':path})
    msg = zope.i18n.translate(aux, context=context.request)
    LOG(PROJECTNAME, INFO, msg)

    counter = 0
    # I now have all persons in my results, so i should start adding them to site
    for organization in results:
        if context.get(organization['id']):

            aux = _("There's already an organization with this id here.")
            msg = zope.i18n.translate(aux, context=context.request)
            LOG(PROJECTNAME, WARNING, msg)

            aux = _('You will have to load the organization with id '
                    '${organization_id} manually.',\
                    mapping={'organization_id':organization['id']})
            msg = zope.i18n.translate(aux, context=context.request)
            LOG(PROJECTNAME, WARNING, msg)

        else:
            try:
                context.invokeFactory('Organization', organization['id'])
                new_organization = context.get(organization['id'])
                for attr in organization.keys():
                    if attr != 'id':
                        setattr(new_organization, attr, organization[attr])
                counter += 1
                portal_catalog.reindexObject(new_organization)

                aux = _('Successfuly added ${organization_id}.',\
                        mapping={'organization_id':organization['id']})
                msg = zope.i18n.translate(aux, context=context.request)
                LOG(PROJECTNAME, INFO, msg)

            except:
                aux = _('There was an error while adding.')
                msg = zope.i18n.translate(aux, context=context.request)
                LOG(PROJECTNAME, WARNING, msg)

                aux = _('You will have to load the organization with id '
                        '${organization_id} manually.',\
                        mapping={'organization_id':organization['id']})
                msg = zope.i18n.translate(aux, context=context.request)
                LOG(PROJECTNAME, WARNING, msg)

    aux = _('Successfuly added ${organizations_number} organizations to ${location}.',\
            mapping={'organizations_number':counter,
                     'location':path})
    msg = zope.i18n.translate(aux, context=context.request)
    LOG(PROJECTNAME, INFO, msg)

    return counter