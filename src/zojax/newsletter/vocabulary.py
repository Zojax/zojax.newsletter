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
from zope import interface
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import INewsletterProduct


class NewslettersVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        product = getUtility(INewsletterProduct)

        terms = []
        for name, newsletter in product.items():
            terms.append(
                (newsletter.title, SimpleTerm(name, name, newsletter.title)))

        terms.sort()
        return SimpleVocabulary([term for title, term in terms])
