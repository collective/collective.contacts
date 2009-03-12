"""Common configuration constants
"""

GLOBALS = globals()
try:
    import Products.CMFPlone.migrations.v3_0
    PLONE3 = True
except ImportError:
    PLONE3 = False
    
PROJECTNAME = 'collective.contacts'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Group': 'collective.contacts: Add Group',
    'Organization': 'collective.contacts: Add Organization',
    'Person': 'collective.contacts: Add Person',
    'Address Book': 'collective.contacts: Add Address Book',
}
