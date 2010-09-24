from zope.interface import implements
from zope.component import adapts
from Products.CMFPlone.utils import safe_unicode
from Products.Archetypes.interfaces import IObjectPostValidation
from Products.statusmessages.interfaces import IStatusMessage

from collective.contacts.interfaces import IOrganization, IPerson
from collective.contacts import contactsMessageFactory as _

class ValidateOrganizationName(object):
    """
    Checks ...
    """
    implements(IObjectPostValidation)
    adapts(IOrganization)
    field_name = 'title'
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, request):
        messages = IStatusMessage(request)
        value = request.form.get(self.field_name,
                                 request.get(self.field_name, None))
        
        if value is not None:
            organization = self.context.portal_catalog.searchResults(portal_type='Organization', Title=value)
            if organization:
                if len(organization) == 1 and \
                    organization[0].getObject().REQUEST.form['id'] == request.form['id']:
                    pass
                else:
                    request.form['show_checkbox'] = True;
                    if ('add_anyway' not in request.form) or \
                       (not request.form['add_anyway']):
                        messages.addStatusMessage(_(u'There is already an'
                            'organization with that name. If you want to'
                            'proceed anyway, please check the box below.'),
                            type="error")
                        return { self.field_name: '' }
        
        return None


class ValidatePersonName(object):
    """
    Checks ...
    """
    implements(IObjectPostValidation)
    adapts(IPerson)
    field_name_1 = 'firstName'
    field_name_2 = 'lastName'
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, request):
        messages = IStatusMessage(request)
        value_1 = request.form.get(self.field_name_1,
                                request.get(self.field_name_1, None))
        value_2 = request.form.get(self.field_name_2,
                                request.get(self.field_name_2, None))
            
        if value_1 is not None and value_2 is not None:
            person = self.context.portal_catalog.searchResults(
                             portal_type='Person',
                             Title=safe_unicode(', '.join([value_1, value_2])))
            if person:
                if len(person) == 1 and \
                    person[0].getObject().REQUEST.form['id'] == request.form['id']:
                    pass
                else:
                    request.form['show_checkbox'] = True;
                    if ('add_anyway' not in request.form) or \
                       (not request.form['add_anyway']):
                        msg = _(u'There is already a Person with that name and last'
                                'name. If you want to proceed anyway, please check the'
                                'box below.')
                        messages.addStatusMessage(msg, type="error")
                        return { self.field_name_1: '',
                                 self.field_name_2: '' }
        
        return None
