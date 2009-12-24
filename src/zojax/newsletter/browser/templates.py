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
from zope import component
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.security.management import queryInteraction

from zojax.statusmessage.interfaces import IStatusMessage

from zojax.mail.interfaces import IMailAddress
from zojax.mailtemplate.base import MailTemplateBase
from zojax.mailtemplate.template import MailPageTemplate
from zojax.subscription.interfaces import IPrincipalSubscribedEvent

from zojax.newsletter.interfaces import _, INewsletter


class SubscriptionTemplate(MailTemplateBase):

    charset = 'utf-8'
    contentType = 'text/html'
    template = MailPageTemplate('templatesubscribtion.pt')

    @property
    def subject(self):
        return 'Newsletter subscription: %s'%self.context.title

    def update(self):
        self.newsletters_prefs_url = '%s/preferences/newsletters/'%(
            absoluteURL(getSite(), self.request))


class HtmlNewsletter(MailTemplateBase):

    charset = 'utf-8'
    contentType = 'text/html'

    @property
    def subject(self):
        return self.context.title

    def render(self):
        return self.context.html.cooked


class TextNewsletter(MailTemplateBase):

    charset = 'utf-8'
    contentType = 'text/plain'

    @property
    def subject(self):
        return self.context.title

    def render(self):
        return self.context.plain



@component.adapter(INewsletter, IPrincipalSubscribedEvent)
def principalSubscribedEvent(newsletter, event):
    request = getRequest()
    if request is None:
        return

    principal = event.principal

    mail = IMailAddress(principal, None)
    if mail is not None:
        template = SubscriptionTemplate(newsletter, request)
        template.update()

        try:
            template.send((mail.address,), principal=principal)
        except:
            IStatusMessage(request).add(
                _("Can't send confirmation email."), 'warning')


def getRequest():
    interaction = queryInteraction()

    if interaction is not None:
        for request in interaction.participations:
            return request
