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
from BTrees.OOBTree import OOBTree

from zope import interface, component
from zope.security.proxy import removeSecurityProxy
from zope.cachedescriptors.property import Lazy
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zojax.content.type.interfaces import IOrder
from zojax.content.type.order import AnnotatableOrder
from zojax.content.type.container import ContentContainer

from interfaces import INewsletter, INewsletterEntry


class Newsletter(ContentContainer):
    interface.implements(INewsletter)

    _SampleContainer__data = ()


class NewsletterOrder(AnnotatableOrder):
    component.adapts(Newsletter)

    def initialize(self):
        data = [OOBTree(), OOBTree()]
        self.annotations[self.ANNOTATION_KEY] = data
        self.order, self.border = data

    def generateKey(self, item):
        return (item.date, item.__name__)


@component.adapter(INewsletterEntry, IObjectModifiedEvent)
def entryModifiedHandler(entry, event):
    order = IOrder(removeSecurityProxy(entry.__parent__))
    order.removeItem(entry.__name__)
    order.addItem(entry.__name__)
