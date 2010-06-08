from zope.component import getAdapter, getAdapters
from plone.memoize.instance import memoize

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.contacts.interfaces import IImport
from collective.contacts import contactsMessageFactory as _

class ImportView(BrowserView):
    """
    Import browser view
    """

    pt = ViewPageTemplateFile('./templates/import.pt')
    labels = {'person': _('label_persons', default=u'Persons'),
              'organization': _('label_organizations', default=u'Organizations'),
              'group': _(u'Groups')}

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.message = None
        submitted = self.request.form.get('import.submitted', False)

        if submitted:
            import_type = self.request.form.get('import_selection', False)
            import_file = self.request.form.get('import_file')
            
            statusmessage = IStatusMessage(self.request)
            
            if not import_file:
                statusmessage.addStatusMessage(_(u'Please select a file to import'), 'error')
            else:
                # Call the import method
                handler = getAdapter(self.context, interface=IImport, name=import_type)
                imported = handler.importFile(import_file)
                
                statusmessage.addStatusMessage(handler.successMsg(imported), 'info')
        
        return self.pt()
    
    @memoize
    def importFormats(self):
        return [{'value': name,
                 'title': self.labels.get(name.split('.')[0], name.split('.')[0]),
                 'format': adapter.title} for name, adapter in getAdapters((self.context,), IImport) if len(name.split('.'))>1]
