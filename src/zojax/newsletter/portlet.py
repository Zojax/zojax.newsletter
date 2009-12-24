##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zojax.subscription.interfaces import ISubscription
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, INewsletterProduct


class NewsletterPortlet(object):

    nlObjects = None

    def update(self):
        super(NewsletterPortlet, self).update()

        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return

        product = getUtility(INewsletterProduct)
        if not product.isInstalled():
            return

        newsletters = []
        for nId in self.newsletters:
            nl = product.get(nId)
            if nl is not None:
                newsletters.append((nl.title, nl))

        newsletters.sort()
        self.nlObjects = [nl for t, nl in newsletters]

        if 'portlet.newsletters.update' in self.request:
            updated = False
            nlids = self.request.get('portlet.newsletters', ())

            for nl in self.nlObjects:
                subs = ISubscription(nl)
                if nl.__name__ in nlids:
                    if not subs.isSubscribed():
                        subs.subscribe()
                        updated = True
                else:
                    if subs.isSubscribed():
                        subs.unsubscribe()
                        updated = True

            if updated:
                IStatusMessage(self.request).add(
                    _('Newsletter subscriptions have been updated.'))

        self.portal_url = absoluteURL(getSite(), self.request)

    def listNewsletters(self):
        for nl in self.nlObjects:
            subs = ISubscription(nl)

            data = {'id': nl.__name__,
                    'title': nl.title,
                    'subscription': subs.isSubscribed()}
            yield data

    def isAvailable(self):
        return bool(self.nlObjects)
