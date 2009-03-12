#!/bin/sh

#This script is used because i18ndude does not get translation from some files
#For example *.zcml
#So the idea is you add your manual translation strings in locales/manual.pot
#And after executing this script, the locales/collective.contacts.pot
#will include all strings gathered with i18ndude, plus the ones inside
#locales/manual.pot
#In addition, it will update the .po files

i18ndude rebuild-pot --pot locales/collective.contacts.pot --merge locales/manual.pot --create collective.contacts .
i18ndude sync --pot locales/collective.contacts.pot locales/*/LC_MESSAGES/collective.contacts.po
