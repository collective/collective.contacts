# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import zope.i18n

from collective.contacts.content.organization import Organization
from collective.contacts.content.person import Person

class ICustomizeView(Interface):
    """
    Customize view interface
    """

class CustomizeView(BrowserView):
    """
    Customize browser view
    """
    implements(ICustomizeView)

    pt = ViewPageTemplateFile('./templates/customizeview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        contenttype = self.request.form.get('customize.type', False)
        cancelled = self.request.form.get('form.button.cancel', False)
       
        if cancelled:
            if contenttype == 'Organization':
                url = self.context.absolute_url() + \
                    '/organizations'
            elif contenttype == 'Person':
                url = self.context.absolute_url() + \
                    '/persons'
            return self.request.response.redirect(url)
        
        submitted = self.request.form.get('customize.submitted', False)

        if submitted:
            columns = self.request.form.get('columns', [])
            selected = self.request.form.get('selected', [])
            new_columns = []
            
            for i in columns:
                new_columns.append((i,i in selected))
                
            if contenttype:
                if contenttype == 'Organization':
                    self.context.show_on_organizations_view = new_columns
                    url = self.context.absolute_url() + \
                                '/organizations'
                elif contenttype == 'Person':
                    self.context.show_on_persons_view = new_columns
                    url = self.context.absolute_url() + \
                                '/persons'
                #url = self.context.absolute_url() + \
                      #'/customize_view?type=%s' % (contenttype,)
                return self.request.response.redirect(url)

        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_columns(self, contenttype=None):
        """
        This method is used to get all fields from the CT, being persons
        or organizations. This will return a list of tuples in the form
        (id, name, bool) where id is the field id, name is the field name,
        and bool is wether this field is selected to be shown in the table
        view or not.
        """
        get_schema = {'Organization':Organization.schema,
                      'Person':Person.schema}

        get_selected = {'Organization':self.context.show_on_organizations_view,
                        'Person':self.context.show_on_persons_view}

        results = []
        if not contenttype:
            contenttype = self.request.form.get('customize.type', None)
            
        if contenttype:
            schema = get_schema[contenttype]
            selected = get_selected[contenttype]

            for i in selected:
                field_id = i[0]
                name = schema.get(field_id).widget.label
                field = (field_id, name, i[1])
                results.append(field)

        return results