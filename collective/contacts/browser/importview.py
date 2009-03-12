from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.imports import importCSVPersons, importCSVOrganizations

import zope.i18n


class IImportView(Interface):
    """
    Import view interface
    """

class ImportView(BrowserView):
    """
    Import browser view
    """
    implements(IImportView)

    pt = ViewPageTemplateFile('./templates/importview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        submitted = self.request.form.get('import.submitted', False)

        if submitted:
            import_type = self.request.form.get('import_selection', False)
            import_file = self.request.form.get('import_file')
            path = '/'.join(self.context.getPhysicalPath())

            if import_type == 'persons':
                # Call the persons import method
                imported = importCSVPersons(self.context, path, import_file)

                aux = _(u'%s successfuly imported persons')
                status = zope.i18n.translate(aux, context=self.request)

                url = self.context.absolute_url() + \
                      '/import_view?message=%s' % (status%imported,)
                return self.request.response.redirect(url)

            elif import_type == 'organizations':
                # Call the organizations import method
                imported = importCSVOrganizations(self.context, path, import_file)
                aux = _(u'%s successfuly imported organizations')
                status = zope.i18n.translate(aux, context=self.request)

                url = self.context.absolute_url() + \
                      '/import_view?message=%s' % (status%imported,)
                return self.request.response.redirect(url)

            else:
                pass
        
        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
