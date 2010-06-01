# -*- coding: utf-8 -*-
from Acquisition import aq_inner

from zope.component import _api as zapi
from collective.contacts.interfaces import ICountriesStates
from collective.contacts.vocabularies import TitledVocabulary

from zope.interface import implements

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView

from collective.contacts import contactsMessageFactory as _

import zope.i18n

class KSSModifySelector(PloneKSSView):


    implements(IPloneKSSView)
    def kssModifyState(self, country=None, search=0):
        """
        This method is used to update the province drop down when adding
        a person or organization and also from the advanced search template
        that's why it has some ugly logic. Perhaps should be divided
        in two methods, one that gets called from the ct, and another one
        that gets called from the search template
        """
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        utility = zapi.getUtility(ICountriesStates)

        if not search and not country:
            # This is necessary for the inline edition
            country = context.getCountry()

        if country and country != '--':
            # I will be here if the country has -- selected, in which case
            # i should return all states possible
            results = TitledVocabulary.fromTitles(utility.states(country=country))
        else:
            # I will be here if the country has something selected, in which
            # case i should return a filtered state list
            results = TitledVocabulary.fromTitles(utility.states())

        if search:
            selector = ksscore.getHtmlIdSelector('form.state')
            result_html = u'<select name="form.state" id="form.state">'
        else:
            selector = ksscore.getHtmlIdSelector('state')
            result_html = u'<select name="state" id="state">'
        
        for i in results._terms:
            aux = _(i.value)
            value = zope.i18n.translate(aux, context=self.request)
            aux = _(i.title)
            title = zope.i18n.translate(aux, context=self.request)
            if not search and context.state == value:
                result_html += (u'<option value="%s" selected="True">%s'
                                 '</option>' % (value,title))
            else:
                result_html += (u'<option value="%s">%s</option>'
                                                % (value,title))

        result_html += u'</select>'

        # I replace the existing drop down
        ksscore.replaceHTML(selector, result_html)

        # and finally we render
        return self.render()

    def kssModifySector(self, sector=None, search=0):
        """
        This method is used to update the sub sector drop down when adding
        an organization and also from the advanced search template that's why
        it has some ugly logic. Perhaps should be divided in two methods, one
        that gets called from the ct, and another one that gets called from
        the search template
        """

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        if search:
            # If i'm here means i'm inside the search template
            address_book = context
        else:
            # If i'm here means i'm inside some ct
            address_book = context.aq_parent
            if not sector:
                # This is necessary for the inline edition
                sector = context.getSector()

        if not sector or sector == '--':
            # If i'm here, means someone selected the -- sector, in which
            # case, i should return all sub sectors available
            sub_sectors = address_book.get_all_sub_sectors()
        else:
            # If i'm here, means someone selected some sector, in which case,
            # i should return a filtered sub sector list
            sub_sectors = address_book.get_sub_sectors(sector)
        results = TitledVocabulary.fromTitles([('--',_(u'(no value)'))] + zip(sub_sectors, sub_sectors))
        
        if search:
            selector = ksscore.getHtmlIdSelector('form.sub_sector')
            # If i'm here means i'm inside the advanced search template
            # so i create the html needed for the sub sector drop down
            result_html = u'<select name="form.sub_sector" id="form.sub_sector" size="1">'
        else:
            selector = ksscore.getHtmlIdSelector('sub_sector')
            # If i'm here, means i'm inside some ct, then i create the html
            # for the drop down
            result_html = u'<select name="sub_sector" id="sub_sector">'

        for i in results._terms:
            if not search and context.sub_sector == i.value:
                result_html += (u'<option value="%s" selected="True">%s'
                                '</option>' % (i.value,i.title))
            else:
                result_html += (u'<option value="%s">%s</option>'
                                                    % (i.value,i.title))
        result_html += u'</select>'

        # replace the existing one
        ksscore.replaceHTML(selector, result_html)

        # And finally render
        return self.render()
