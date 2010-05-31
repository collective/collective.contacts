from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _
from collective.contacts.imports import importCSVPersons, importCSVOrganizations

class ImportView(BrowserView):
    """
    Import browser view
    """

    pt = ViewPageTemplateFile('./templates/import.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.message = None
        submitted = self.request.form.get('import.submitted', False)

        if submitted:
            import_type = self.request.form.get('import_selection', False)
            import_file = self.request.form.get('import_file')
            path = '/'.join(self.context.getPhysicalPath())

            if import_type == 'persons':
                # Call the persons import method
                imported = importCSVPersons(self.context, path, import_file)
                self.message = _(u'Successfuly imported ${number} persons', mapping={'number': imported})

            elif import_type == 'organizations':
                # Call the organizations import method
                imported = importCSVOrganizations(self.context, path, import_file)
                self.message = _(u'Successfuly imported ${number} organizations', mapping={'number': imported})
        
        return self.pt()
