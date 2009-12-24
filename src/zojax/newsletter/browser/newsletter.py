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
from zojax.batching.batch import Batch
from zojax.content.type.interfaces import IOrder
from zojax.content.type.interfaces import IContentViewView
from zojax.newsletter.interfaces import INewsletter


class NewsletterView(object):

    def update(self):
        order = IOrder(self.context)

        self.entries = Batch(order, size=2, request=self.request)


class NewsletterViewView(object):
    interface.implements(IContentViewView)
    component.adapts(INewsletter, interface.Interface)

    name = u'context.html'

    def __init__(self, nl, request):
        pass
