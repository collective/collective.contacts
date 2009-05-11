# -*- coding: utf-8 -*-
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

def reindexCatalog(context):
    """
    This method will reindex the 2 new indexes added to the catalog
    """
    from Products.CMFCore.utils import getToolByName
    site = context.getSite()
    cat = getToolByName(site, 'portal_catalog')
    cat.reindexIndex('lastName', site.REQUEST)
    cat.reindexIndex('firstName', site.REQUEST)
