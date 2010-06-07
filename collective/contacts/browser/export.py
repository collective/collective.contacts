from zope.component import getAdapter

from Products.Five import BrowserView

from collective.contacts.interfaces import IExport

class ExportView(BrowserView):
    """ Export browser view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def vcard(self):
        handler = getAdapter(self.context, interface=IExport, name='%s.vcard' % self.context.meta_type.lower())
        return handler.export(self.request)
    
    def vcalendar(self):
        handler = getAdapter(self.context, interface=IExport, name='%s.vcalendar' % self.context.meta_type.lower())
        return handler.export(self.request)
