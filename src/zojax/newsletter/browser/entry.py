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
from email.Header import make_header
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formataddr, formatdate
from email import message_from_string

from zope import schema, interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from z3c.schema.email import RFC822MailAddress
from zojax.layoutform import button, Fields, PageletEditForm
from zojax.content.forms.form import AddForm
from zojax.newsletter.interfaces import _
from zojax.mail.interfaces import IMailer, IMailAddress
from zojax.mailtemplate.interfaces import IMailMessage
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.subscription.interfaces import ISubscribersManagement

from zojax.newsletter.browser import templates


class AddNewsletterEntry(AddForm):

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


class ISendTesting(interface.Interface):

    email = RFC822MailAddress(
        title = _(u'Destination'),
        description = _(u'Testing destination email address.'),
        required = True)


class SendNewsletter(PageletEditForm):

    label = _('Send testing newsletter')

    fields = Fields(ISendTesting)

    ignoreContext = True

    def update(self):
        super(SendNewsletter, self).update()

        if 'form.send' in self.request:
            subs = ISubscribersManagement(self.context.__parent__)

            emails = []
            for principal in subs.getSubscribers():
                mail = IMailAddress(principal, None)
                if mail is not None:
                    email = mail.address

                    if email:
                        emails.append(
                            formataddr((principal.title or principal.id, email)))

            if emails:
                message = self.generateMessage()
                message['Subject'] = make_header(((self.context.title, 'utf-8'),))

                mailer = getUtility(IMailer)

                from_address = str(formataddr(
                    (mailer.email_from_name, mailer.email_from_address)))

                message['From'] = from_address
                mailer.send(from_address, emails, message.as_string())

                IStatusMessage(self.request).add(_('Newsletter has been sent.'))

    def generateMessage(self):
        context = self.context

        message = MIMEMultipart('alternative')
        message['Date'] = formatdate()

        textMail = IMailMessage(
            templates.TextNewsletter(context, self.request))()
        message.attach(message_from_string(textMail))

        if context.html:
            htmlMail = IMailMessage(
                templates.HtmlNewsletter(context, self.request))()
            message.attach(message_from_string(htmlMail))
        return message

    @button.buttonAndHandler(_(u'Send testing newsletter'), name='testing')
    def handleSendTesting(self, action):
        data, errors = self.extractData()
        if errors:
            IStatusMessage(self.request).add(
                (self.formErrorsMessage,) + errors, 'formError')
        else:
            message = self.generateMessage()
            message['Subject'] = make_header(
                ((u'Test message: %s'%self.context.title, 'utf-8'),))

            mailer = getUtility(IMailer)

            from_address = formataddr(
                (mailer.email_from_name, mailer.email_from_address))
            mailer.send(from_address, (data['email'],), message.as_string())

            IStatusMessage(self.request).add(
                _('Test mail for newsletter has been sent.'))
