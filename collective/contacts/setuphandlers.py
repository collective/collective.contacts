# -*- coding: utf-8 -*-
INDEXES = ['shortName',
           'firstName',
           'lastName',
           'birthdate',
           'organization',
           'sortable_organization',
           'position',
           'department',
           'address',
           'country',
           'state',
           'city',
           'zip',
           'sector',
           'sub_sector',
           'members',
           ]

def importVarious(context):
    """
    Import various settings for collective.contacts
    copied from Products.ATExtensions

    This provisional handler will be removed again as soon as
    full handlers are implemented for this step.
    """
    if context.readDataFile('collective.contacts_various.txt') is None:
        return
    
    site = context.getSite()
    pfc = site.portal_form_controller
    pfc.addFormValidators('atct_edit',
                          '',   # context_type
                          'more',
                          '')   # validators
    pfc.addFormAction('atct_edit',
                      'success',
                      '',    # context_type
                      'more',
                      'traverse_to',
                      'string:more_edit')
    return "Added validator and action for the 'more' button to " \
           "the form controller."

def reindexCatalog(context):
    """
    This method will reindex the 3 new indexes added to the catalog
    """
    if context.readDataFile('collective.contacts_reindex.txt') is None:
        return
    
    from Products.CMFCore.utils import getToolByName
    site = context.getSite()
    cat = getToolByName(site, 'portal_catalog')
    indexes = cat.indexes()
    for index in INDEXES:
        if index in indexes:
            cat.reindexIndex(index, site.REQUEST)
