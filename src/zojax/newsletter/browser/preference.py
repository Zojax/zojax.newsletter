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
from zojax.subscription.interfaces import ISubscription
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.newsletter.interfaces import _, INewsletterProduct


class NewslettersPreference(object):

    def update(self):
        request = self.request
        product = getUtility(INewsletterProduct)

        if 'subscribe' in request:
            newsletter = product.get(request.get('subscribe', ''))
            if newsletter is not None:
                subs = ISubscription(newsletter)
                subs.subscribe()
                IStatusMessage(request).add(
                    _('You have been subscribed to newsletter.'))
                return self.redirect('./')

        if 'unsubscribe' in request:
            newsletter = product.get(request.get('unsubscribe', ''))
            if newsletter is not None:
                subs = ISubscription(newsletter)
                subs.unsubscribe()
                IStatusMessage(request).add(
                    _('You have been unsubscribed from newsletter.'))
                return self.redirect('./')

        newsletters = []
        for key, nl in product.items():
            subs = ISubscription(nl)

            newsletters.append(
                (nl.title,
                 {'id': nl.__name__,
                  'title': nl.title,
                  'description': nl.description,
                  'subscribed': subs.isSubscribed(),
                  'newsletter': nl}))

        newsletters.sort()
        self.newsletters = [nl for title, nl in newsletters]
