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
from zojax.controlpanel.storage import ConfigletData
from zojax.controlpanel.interfaces import IConfigletDataFactory

from interfaces import INewsletterProduct


class NewsletterData(ConfigletData):
    interface.implements(interface.Interface)


class NewsletterDataFactory(object):
    component.adapts(INewsletterProduct)
    interface.implements(IConfigletDataFactory)

    def __init__(self, configlet):
        self.configlet = configlet

    def __call__(self, *args, **kw):
        return NewsletterData(*args, **kw)
