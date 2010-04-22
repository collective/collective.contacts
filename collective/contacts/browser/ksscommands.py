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
    def kssModifyState(self, country=None):
        """
        This method is used to update the province drop down when adding
        a person or organization and also from the advanced search template
        that's why it has some ugly logic. Perhaps should be divided
        in two methods, one that gets called from the ct, and another one
        that gets called from the search template
        """

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        selector = ksscore.getHtmlIdSelector('state')

        utility = zapi.getUtility(ICountriesStates)

        if not country:
            # This is necesary for the inline edition
            country = context.getCountry()

        if country != '--':
            # I will be here if the country has -- selected, in which case
            # i should return all states possible
            results = TitledVocabulary.fromTitles(utility.states(country=country))
        else:
            # I will be here if the country has something selected, in which
            # case i should return a filtered state list
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
            # If i'm here, means this is some content type
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

        # I replace the existing drop down
        ksscore.replaceHTML(selector, result_html)

        # and finally we render
        return self.render()

    def kssModifySector(self, sector=None):
        """
        This method is used to update the sub sector drop down when adding
        an organization and also from the advanced search template that's why
        it has some ugly logic. Perhaps should be divided in two methods, one
        that gets called from the ct, and another one that gets called from
        the search template
        """

        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')

        selector = ksscore.getHtmlIdSelector('sub_sector')

        if context.meta_type == 'AddressBook':
            # If i'm here means i'm inside the search template
            address_book = context
        else:
            # If i'm here means i'm inside some ct
            address_book = context.aq_parent

        if not sector:
            # This is necesary for the inline edition
            sector = context.getSector()

        if sector == '--':
            # If i'm here, means someone selected the -- sector, in which
            # case, i should return all sub sectors available
            sub_sectors = address_book.get_all_sub_sectors()
            results = TitledVocabulary.fromTitles(
                                            zip(sub_sectors, sub_sectors))
        else:
            # If i'm here, means someone selected some sector, in which case,
            # i should return a filtered sub sector list
            sub_sectors = address_book.get_sub_sectors(sector)
            results = TitledVocabulary.fromTitles(zip(sub_sectors, sub_sectors))

        if context.meta_type == 'AddressBook':
            # If i'm here means i'm inside the advanced search template
            # so i create the html needed for the sub sector drop down
            result_html = u'<select name="sub_sector" id="sub_sector">'
            result_html += (u'<option value="--">--</option>')
            for i in results._terms:
                result_html += (u'<option value="%s">%s</option>'
                                                    % (i.value,i.title))
            result_html += u'</select>'

        else:
            # If i'm here, means i'm inside some ct, then i create the html
            # for the drop down
            result_html = u'<select name="sub_sector" id="sub_sector">'
            for i in results._terms:
                if context.sub_sector == i.value:
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
