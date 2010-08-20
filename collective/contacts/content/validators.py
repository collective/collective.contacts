from zope.interface import implements
from zope.component import adapts
from Products.CMFPlone.utils import safe_unicode
from Products.Archetypes.interfaces import IObjectPostValidation
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
        value = request.form.get(self.field_name,
        request.get(self.field_name, None))
        
        if ('skip_validator' in request.form) and \
           request.form['skip_validator']:
            return None
            
        if value is not None:
            organization = self.context.portal_catalog.searchResults(
            portal_type='Organization', Title=value)
            if organization:
                request.form['show_checkbox'] = True;
                if ('add_anyway' not in request.form) or \
                   (not request.form['add_anyway']):
                    return { self.field_name: _(u'There is already an \
                    organization with that name. If you want to \
                    proceed anyway, please check the box below.') }
            elif 'skip_validator' in request.form:
                request.form['skip_validator'] = True
        
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
        value_1 = request.form.get(self.field_name_1,
        request.get(self.field_name_1, None))
        value_2 = request.form.get(self.field_name_2,
        request.get(self.field_name_2, None))
        
        if ('skip_validator' in request.form) and \
           request.form['skip_validator']:
            return None
            
        if value_1 is not None and value_2 is not None:
            person = self.context.portal_catalog.searchResults(
                     portal_type='Person',
                     Title=safe_unicode(', '.join([value_1, value_2])))
            if person:
                request.form['show_checkbox'] = True;
                if ('add_anyway' not in request.form) or \
                   (not request.form['add_anyway']):
                    msg = _(u'There is already a Person with that name and last \
                          name. If you want to proceed anyway, please check the \
                          box below.')
                    return { self.field_name_1: msg,
                             self.field_name_2: msg }
            elif 'skip_validator' in request.form:
                request.form['skip_validator'] = True
        
        return None
