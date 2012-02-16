from zope.formlib import form
from zope.app.form.browser import DropdownWidget

from Products.Five.formlib.formbase import PageForm

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IPerson, IOrganization

class CustomDropdownWidget(DropdownWidget):
    _displayItemForMissingValue = False
def CustomDropdownWidgetFactory(field, request):
    return CustomDropdownWidget(field, field.vocabulary, request)

class FindOrganizationForm(PageForm):
    form_fields = form.FormFields(IOrganization).omit('email2', 'email3')
    form_fields['country'].custom_widget = CustomDropdownWidgetFactory
    form_fields['state'].custom_widget = CustomDropdownWidgetFactory
    form_fields['sector'].custom_widget = CustomDropdownWidgetFactory
    form_fields['sub_sector'].custom_widget = CustomDropdownWidgetFactory
    label = _('advanced_organizations_search', default=u'Advanced organizations search:')
    
    def __call__(self):
        self.request.set('disable_border', 1)
        # change the form action the point to the search page
        self.request.set('URL', '%s/search_organization' % self.context.absolute_url())
        return super(FindOrganizationForm, self).__call__()

    @form.action(_('label_search_organizations', default=u'Search Organizations'))
    def action_search(self, action, data):
        pass

    @form.action(_('label_cancel', default=u'Cancel'))
    def action_cancel(self, action, data):
        pass

class FindPersonForm(PageForm):
    form_fields = form.FormFields(IPerson).omit('workEmail2', 'workEmail3', 'photo', 'organization', 'birthdate')
    form_fields['country'].custom_widget = CustomDropdownWidgetFactory
    form_fields['state'].custom_widget = CustomDropdownWidgetFactory
    label = _('advanced_persons_search', default=u'Advanced persons search:')
    
    def __call__(self):
        self.request.set('disable_border', 1)
        self.form_fields['firstName'].field.required = False
        self.form_fields['lastName'].field.required = False
        # change the form action the point to the search page
        self.request.set('URL', '%s/search_person' % self.context.absolute_url())
        return super(FindPersonForm, self).__call__()

    @form.action(_('label_search_persons', default=u'Search Persons'))
    def action_search(self, action, data):
        pass

    @form.action(_('label_cancel', default=u'Cancel'))
    def action_cancel(self, action, data):
        pass
