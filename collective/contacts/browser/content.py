# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from zope.component import getMultiAdapter

class ContentActionsViewlet(ViewletBase):
    def update(self):
        super(ContentActionsViewlet, self).update()

        context = aq_inner(self.context)
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
                                             
        actions = self.context_state.actions()
        
        action_list = []
        if self.context_state.is_structural_folder():
            action_list = actions['folder'] + actions['object']
        else:
            action_list = actions['object']

        self.fallback = 'view'
        try:
            default_view = context.getLayout()
            for action in action_list:
                if default_view == action['id']:
                    self.fallback = action['id']
        except:
            pass


    index = ViewPageTemplateFile("templates/contentviews.pt")
