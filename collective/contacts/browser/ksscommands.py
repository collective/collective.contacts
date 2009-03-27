from Acquisition import aq_inner

from zope.app import zapi
from collective.contacts.interfaces import ICountriesStates
from collective.contacts.vocabularies import TitledVocabulary

from zope.interface import implements

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView

from collective.contacts import contactsMessageFactory as _

import zope.i18n

class KSSModifySelector(PloneKSSView):

    
    implements(IPloneKSSView)
    def kssModifyState(self, country):

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        selector = ksscore.getHtmlIdSelector('state')

        utility = zapi.getUtility(ICountriesStates)
        if country != '--':
            results = TitledVocabulary.fromTitles(utility.states(country=country))
        else:
            results = TitledVocabulary.fromTitles(utility.states())

        if context.meta_type == 'AddressBook':
            # If we are here, means this is a search template
            result_html = u'<select name="state" id="state">'
            result_html += (u'<option value="--">--</option>')
            
            for i in results._terms:
                if (i.value == u'(no values)' or i.value == u'??NA'):
                    continue
                aux = _(i.value)
                value = zope.i18n.translate(aux, context=self.request)
                aux = _(i.title)
                title = zope.i18n.translate(aux, context=self.request)
                result_html += (u'<option value="%s">%s</option>'
                                                    % (value,title))
            result_html += u'</select>'

        if (context.meta_type == 'Person' or
            context.meta_type == 'Organization'):

            result_html = u'<select name="state" id="state">'
            for i in results._terms:
                aux = _(i.value)
                value = zope.i18n.translate(aux, context=self.request)
                aux = _(i.title)
                title = zope.i18n.translate(aux, context=self.request)
                if context.state == value:
                    result_html += (u'<option value="%s" selected="True">%s'
                                     '</option>' % (value,title))
                else:
                    result_html += (u'<option value="%s">%s</option>'
                                                    % (value,title))

            result_html += u'</select>'

        ksscore.replaceHTML(selector, result_html)

        
        return self.render()

    def kssModifySector(self, sector):

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        selector = ksscore.getHtmlIdSelector('sub_sector')

        address_book = context.aq_parent
        results = TitledVocabulary.fromTitles(
                                           address_book.get_sub_sectors(sector))

        result_html = u'<select name="sub_sector" id="sub_sector">'
        for i in results._terms:
            if context.sub_sector == i.value:
                result_html += (u'<option value="%s" selected="True">%s'
                                 '</option>' % (i.value,i.title))
            else:
                result_html += (u'<option value="%s">%s</option>'
                                                            % (i.value,i.title))

        ksscore.replaceHTML(selector, result_html)

        return self.render()
