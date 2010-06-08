from collective.contacts import contactsMessageFactory as _
from collective.contacts.browser.list import PersonListView, GroupListView

class GroupView(PersonListView):
    """ Displays information about a group
    """
    error_msg = _('no_persons_in_group', default=u'There are no persons assigned to this group')

    @property
    def title(self):
        return self.context.Title()
    
class GroupGroupsView(GroupListView):
    """ Lists groups in a group
    """
    error_msg = _('no_subgroups_in_group', default=u'There are no sub groups in this group')
