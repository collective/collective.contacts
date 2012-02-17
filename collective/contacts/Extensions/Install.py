# -*- coding: utf-8 -*-

def uninstall(portal, reinstall=False):
    setup_tool = portal.portal_setup
    setup_tool.setBaselineContext('profile-collective.contacts:uninstall')
    setup_tool.runAllImportStepsFromProfile('profile-collective.contacts:uninstall')