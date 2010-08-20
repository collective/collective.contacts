# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.contacts.content.addressbook import AddressBook

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
