# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.contacts import logger

wanted = ['shortName',
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

# form : http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def addKeyToCatalog(context):
    '''Takes portal_catalog and adds a key to it
    @param portal: context providing portal_catalog
    '''
    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')

    indexables = []
    for name in wanted:
        meta_type = 'FieldIndex' 
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)

