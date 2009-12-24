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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.richtext.field import RichText
from zojax.content.type.interfaces import IItem
from zojax.preferences.interfaces import IPreferenceCategory

_ = MessageFactory('zojax.newsletter')


class INewsletter(IItem):
    """ newsletter """


class INewsletterEntry(IItem):
    """ newsletter entry """

    date = schema.Date(
        title = _('Date'),
        description = _('Newsletter entry date.'),
        required = True)

    plain = schema.Text(
        title = u'Plain',
        description = u'Plain text version of newsletter.',
        required = True)

    html = RichText(
        title = u'HTML',
        description = u'HTML version of newsletter.',
        required = False)

    sendDate = interface.Attribute('Send date')

    def send():
        """ send newsletter """


class INewsletters(IItem):
    """ newsletters container """


class INewsletterProduct(interface.Interface):
    """ product """


class INewsletterPortlet(interface.Interface):
    """ newsletter portlet """

    newsletters = schema.List(
        title = _(u'Newsletters'),
        description = _('Select newsletters for portlet.'),
        value_type = schema.Choice(vocabulary = "zojax.newsletters"),
        default = [],
        required = False)


class INewslettersPreference(IPreferenceCategory):
    """ preferences """

    alternativeEmails = schema.Dict(
        title = u'Alternative emails',
        default = {},
        required = False)
