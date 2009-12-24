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
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.location import LocationProxy
from zope.app.container.contained import uncontained

from zojax.controlpanel.configlet import Configlet
from zojax.content.type.interfaces import IOrder
from zojax.content.type.order import AnnotatableOrder
from zojax.content.type.container import ContentContainer

from interfaces import _, INewsletters


class Newsletters(ContentContainer, Configlet):
    interface.implements(INewsletters)

    title = _(u'Newsletters')

    def __init__(self, tests=()):
        Configlet.__init__(self, tests)

    @property
    def _SampleContainer__data(self):
        return self.data

    def get(self, key, default=None):
        item = super(Newsletters, self).get(key, default)

        if item is default:
            return item

        return LocationProxy(removeAllProxies(item), self, key)

    def __iter__(self):
        for item in self.data.values():
            yield LocationProxy(item, self, item.__name__)

    def __getitem__(self, key):
        item = super(Newsletters, self).__getitem__(key)

        return LocationProxy(removeAllProxies(item), self, key)

    def __delitem__(self, key):
        uncontained(self[key], self, key)
        del self.data[key]


class NewslettersOrder(AnnotatableOrder):
    @component.adapter(INewsletters)

    def __init__(self, context):
        newsletters = removeAllProxies(context)
        super(NewslettersOrder, self).__init__(newsletters.data)

        self.context = newsletters
