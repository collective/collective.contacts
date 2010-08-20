from zope.interface import implements
from zope.component import getAdapter

from plone.app.layout.globals.interfaces import IViewView
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contacts.interfaces import ICustomizableColumns
from collective.contacts import contactsMessageFactory as _

class CustomizeView(BrowserView):
    """
    Customize browser view
    """
    implements(IViewView)

    pt = ViewPageTemplateFile('./templates/customize.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.contenttype = self.request.get('customize.type', False)
        cancelled = self.request.form.get('form.button.cancel', False)
       
        if cancelled or self.contenttype not in ('organization', 'person'):
            return self.redirect()
        
        self.columns = getAdapter(self.context, interface=ICustomizableColumns, name=self.contenttype)
        
        submitted = self.request.form.get('customize.submitted', False)

        if submitted:
            self.columns.set_columns(self.request.form.get('selected', []))
            statusmessage = IStatusMessage(self.request)
            statusmessage.addStatusMessage(_(u'View successfully customized'), 'info')
            return self.redirect()

        return self.pt()
    
    def redirect(self):
        url = self.context.absolute_url()
        if self.contenttype == 'organization':
            url = self.context.absolute_url() + \
                '/organizations'
        elif self.contenttype == 'person':
            url = self.context.absolute_url() + \
                '/persons'
        return self.request.response.redirect(url)

    def get_columns(self):
        """
        This method is used to get all fields from the CT, being persons
        or organizations. This will return a list of dicts in the form
        (id, title, bool) where id is the field id, name is the field name,
        and bool is whether this field is selected to be shown in the table
        view or not.
        """
        return [{'id': column[0],
                 'title': self.columns.translate_column(column[0]),
                 'checked': column[1]} for column in self.columns.get_raw_columns()]
