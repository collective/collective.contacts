from Acquisition import aq_inner

from zope.app import zapi
from collective.contacts.interfaces import ICountriesStates
from collective.contacts.vocabularies import TitledVocabulary

from zope.interface import implements

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView

class KSSModifySelector(PloneKSSView):

    
    implements(IPloneKSSView)
    def kssModifyState(self, country):

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        selector = ksscore.getHtmlIdSelector('state')

        utility = zapi.getUtility(ICountriesStates)
        results = TitledVocabulary.fromTitles(utility.states(country=country))
        result_html = u'<select name="state" id="state">'
        for i in results._terms:
            if context.state == i.value:
                result_html += (u'<option value="%s" selected="True">%s'
                                 '</option>' % (i.value,i.title))
            else:
                result_html += (u'<option value="%s">%s</option>'
                                                            % (i.value,i.title))

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
