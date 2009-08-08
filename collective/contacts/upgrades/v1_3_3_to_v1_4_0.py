# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.contacts.content.addressbook import AddressBook

def addColumns(portal_setup):
    """
    This migration step will include the list of tuples needed to list the
    columns from the views
    """

    portal_catalog = getToolByName(portal_setup, 'portal_catalog')
    address_books = portal_catalog(portal_type='Address Book')
    organizations_columns = AddressBook.show_on_organizations_view
    persons_columns = AddressBook.show_on_persons_view
    
    for i in address_books:
        address_book = i.getObject()
        address_book.show_on_organizations_view = organizations_columns
        address_book.show_on_persons_view = persons_columns

def updatePersonPhotos(portal_setup):
    """
    This migration step will get all persons, and update their photo field
    """

    portal_catalog = getToolByName(portal_setup, 'portal_catalog')
    persons = portal_catalog(portal_type='Person')
    for i in persons:
        person = i.getObject()
        photo_field = person.getField('photo')
        
        photo_field.removeScales(person)
        photo_field.createScales(person)
