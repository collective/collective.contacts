# -*- coding: utf-8 -*-
from StringIO import StringIO
import csv
import time

from collective.contacts.interfaces import ISearch, IPerson, IOrganization

def exportOrganizationsToCSV(context, organizations):
    """
    get a csv with organizations from context.
    """

    text = StringIO()
    writer = csv.writer(text)

    # First, i look for the organizations' fields

    organizations_fields = ["id",
                            "title",
                            "address",
                            "city",
                            "zip",
                            "country",
                            "state",
                            "extra_address",
                            "phone",
                            "fax",
                            "email",
                            "email2",
                            "email3",
                            "web",
                            "sector",
                            "sub_sector",
                            "text"]

    # I add them to the first row in the CSV

    writer.writerow(organizations_fields)
    
    # if no organizations are given fetch all organizations using the search adapter
    if organizations is None:
        search = ISearch(context)
        organizations = search.search({'object_provides': IOrganization.__identifier__})

    # And now, for each organization, i load his data on each column
    for organization in organizations:
        row = []
        for field in organizations_fields:
            row.append(getattr(organization,field))

        writer.writerow(row)

    return text

def exportPersonsToCSV(context, persons):
    """
    get a csv with persons from context.
    """

    text = StringIO()
    writer = csv.writer(text)

    # First, i look for the persons' fields
    # (We will not include the photo in the export, as we cannot export it
    # to a CSV file).

    persons_fields = ["id",
                      "short_name",
                      "first_name", 
                      "last_name", 
                      "organization", 
                      "position", 
                      "department", 
                      "work_phone", 
                      "work_mobile_phone", 
                      "work_email", 
                      "work_email2", 
                      "work_email3", 
                      "address", 
                      "country",
                      "state",
                      "city",
                      "zip",
                      "phone", 
                      "mobile_phone", 
                      "email", 
                      "web", 
                      "text"]

    # I add them to the first row in the CSV

    writer.writerow(persons_fields)
    
    # if no persons are given fetch all persons using the search adapter
    if persons is None:
        search = ISearch(context)
        persons = search.search({'object_provides': IPerson.__identifier__})
    
    # And now, for each person, i load his data on each column

    for person in persons:
        row = []
        for field in persons_fields:
            # there's only one exception, if the field is organizations,
            # we need the organization's name, not the object
            if field == 'organization':
                organization = getattr(person,field)
                if organization:
                    row.append(organization.id)
                else:
                    row.append('')
            else:
                row.append(getattr(person,field))

        writer.writerow(row)

    return text

def setCSVHeaders(request, text, export_type):
    """
    This function will set the request appropriately to return a csv file
    """
    request.RESPONSE.setHeader('Content-Type','application/csv')
    request.RESPONSE.setHeader('Content-Length',len(text.getvalue()))
    request.RESPONSE.setHeader('Content-Disposition',
                               'inline;filename=%s-%s.csv' %(
                               export_type,
                               time.strftime("%Y%m%d-%H%M%S",time.localtime())))

    return request


def exportPersons(context, request, persons=None, format='csv'):
    """
    This function will first get the exported persons, and will load the RESPONSE headers appropriately to return it to the browser and get a nice download dialog.
    """

    # Using this dictionary we do a matching with the format chosen by the user with the appropriate function
    formats = {'csv':exportPersonsToCSV,}
    # And with this other dictionary we do a matching with the format chosen and how the response header should be set.
    headers = {'csv':setCSVHeaders,}

    # We call the importer according to the format chosen by the user. If the format is not available, then a CSV export is done
    text = formats.get(format.lower(), 'csv')(context, persons)

    # Finally we set the response headers so it will open a download dialog
    request = headers.get(format.lower(), 'csv')(request, text, 'persons')

    return text.getvalue()

def exportOrganizations(context, request, organizations=None, format='csv'):
    """
    This function will first get the exported organizations, and will load the RESPONSE headers appropriately to return it to the browser and get a nice download dialog.
    """

    # Using this dictionary we do a matching with the format chosen by the user with the appropriate function
    formats = {'csv':exportOrganizationsToCSV,}
    # And with this other dictionary we do a matching with the format chosen and how the response header should be set.
    headers = {'csv':setCSVHeaders,}

    # We call the importer according to the format chosen by the user. If the format is not available, then a CSV export is done
    text = formats.get(format.lower(), 'csv')(context, organizations)

    # Finally we set the response headers so it will open a download dialog
    request = headers.get(format.lower(), 'csv')(request, text, 'organizations')

    return text.getvalue()
