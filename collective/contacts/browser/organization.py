from collective.contacts import contactsMessageFactory as _
from collective.contacts.browser.list import PersonListView

class OrganizationView(PersonListView):
    """ Displays information about an organization
    """
    error_msg = _('no_persons_in_organization', default=u'There are no persons in this organization')

    @property
    def title(self):
        return _('Persons part of ${organization}', mapping={'organization': self.context.Title()})
