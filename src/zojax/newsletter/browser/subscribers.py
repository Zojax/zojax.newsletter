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
from zope.app.security.interfaces import IAuthentication

from zojax.mail.interfaces import IMailAddress
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.subscription.interfaces import ISubscribersManagement

from zojax.newsletter.interfaces import _


class NewsletterSubscribers(object):

    def listSubscribers(self):
        subs = ISubscribersManagement(self.context)

        subscriptions = []
        for principal in subs.getSubscribers():
            mail = IMailAddress(principal, None)
            if mail is not None:
                email = mail.address
            else:
                email = _('Unknown')

            data = {
                'id': principal.id,
                'title': principal.title,
                'email': email}

            subscriptions.append((data['title'], data))

        subscriptions.sort()
        return [data for t, data in subscriptions]

    def update(self):
        request = self.request

        if 'forum.button.unsubscribe' in request:
            pids = request.get('pids', ())

            if not pids:
                IStatusMessage(request).add(
                    _('Please select principals.'))
            else:
                auth = getUtility(IAuthentication)
                subs = ISubscribersManagement(self.context)

                for pid in pids:
                    subs.unsubscribePrincipal(auth.getPrincipal(pid))

                IStatusMessage(request).add(
                    _('Selected principals have been unsubscribed.'))
