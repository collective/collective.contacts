from collective.contacts import contactsMessageFactory as _
from collective.contacts.browser.list import PersonListView

class GroupView(PersonListView):
    """ Displays information about a group
    """
    error_msg = _('no_persons_in_group', default=u'There are no persons assigned to this group')

    @property
    def title(self):
        return self.context.Title()
