# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, WARNING
from cgi import FieldStorage
from ZPublisher.HTTPRequest import FileUpload
from zope.i18nmessageid import MessageFactory
from config import PROJECTNAME

_ = MessageFactory('collective.importerexporter.utils')

import codecs, cStringIO, csv, DateTime, tarfile, time, StringIO


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

    LOG(PROJECTNAME, INFO, _("Starting the persons import process"))
    
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


    LOG(PROJECTNAME, INFO, _("%s persons to be added to %s"%(counter, path)))

    counter = 0

    # I now have all persons in my results, so i should start adding them to site
    for person in results:
        organization =[i.getObject() for i in portal_catalog(
                                    portal_type = 'Organization',
                                    path = path,
                                    Title = person['organization']
                                    )]


        if organization and len(organization)>1:
            LOG(PROJECTNAME, WARNING, _("There are %s organizations with the same title, i don't know with which one relate this person."%len(organization)))
            LOG(PROJECTNAME, WARNING, _("You will have to load the person with id \"%s\" manually."%person['id']))

        elif organization and len(organization)==1:
            if context.get(person['id']):
                LOG(PROJECTNAME, WARNING, _("There's already a person with this id here."))
                LOG(PROJECTNAME, WARNING, _("You will have to load the person with id \"%s\" manually."%person['id']))
            else:
                try:
                    context.invokeFactory('Person', person['id'])
                    new_person = context.get(person['id'])
                    for attr in person.keys():
                        if attr != 'id' and attr != 'organization':
                            setattr(new_person, attr, person[attr])
                        if attr == 'organization':
                            new_person.setOrganization(organization[0])

                    counter += 1
                    portal_catalog.reindexObject(new_person)
                    LOG(PROJECTNAME, INFO, _("Successfuly added \"%s\"."%person['id']))
                except:
                    LOG(PROJECTNAME, WARNING, _("There was an error while adding."))
                    LOG(PROJECTNAME, WARNING, _("You will have to load the person with id %s manually."%person['id']))
        else:
            LOG(PROJECTNAME, WARNING, _("There's no organization with title %s, make sure it exists before adding persons. \"%s\" not added"%(person['organization'],person['id'])))

    LOG(PROJECTNAME, INFO, _("Successfuly added %s persons to %s."%(counter, path)))

    return counter


def importCSVOrganizations(context, path, file):
    """
    This function is used to import organizations to a given path using a CSV file
    """

    LOG(PROJECTNAME, INFO, _("Starting the organizations import process"))
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

    LOG(PROJECTNAME, INFO, _("%s organizations to be added to %s"%(counter, path)))

    counter = 0
    # I now have all persons in my results, so i should start adding them to site
    for organization in results:
        if context.get(organization['id']):
            LOG(PROJECTNAME, WARNING, _("There's already an organization with this id here."))
            LOG(PROJECTNAME, WARNING, _("You will have to load the organization with id \"%s\" manually."%organization['id']))
        else:
            try:
                context.invokeFactory('Organization', organization['id'])
                new_organization = context.get(organization['id'])
                for attr in organization.keys():
                    if attr != 'id':
                        setattr(new_organization, attr, organization[attr])
                counter += 1
                portal_catalog.reindexObject(new_organization)
                LOG(PROJECTNAME, INFO, _("Successfuly added \"%s\"."%organization['id']))
            except:
                LOG(PROJECTNAME, WARNING, _("There was an error while adding."))
                LOG(PROJECTNAME, WARNING, _("You will have to load the organization with id %s manually."%organization['id']))

    LOG(PROJECTNAME, INFO, _("Successfuly added %s organizations to %s."%(counter, path)))
    return counter