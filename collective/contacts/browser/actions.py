from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.content import DocumentActionsViewlet

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import ICustomizableView

class ContactsActionsViewlet(DocumentActionsViewlet):
    def update(self):
        super(ContactsActionsViewlet, self).update()
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
        self.actions = self.context_state.actions().get('contacts_actions', [])
        if ICustomizableView.providedBy(self.view) and \
           self.view.customize_url() is not None:
            self.actions.append({'id': 'customize',
                                 'title': _(u'customize_view', default=u'Customize view'),
                                 'url': self.view.customize_url(),
                                 'description': ''})

    index = ViewPageTemplateFile('templates/actions.pt')
