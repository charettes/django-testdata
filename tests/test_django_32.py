# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skipIf

import django
from django.test import SimpleTestCase

from testdata import wrap_testdata


@skipIf(django.VERSION < (3, 2), "Django 3.2 only tests.")
class WrapTestDataTests(SimpleTestCase):
    def test_raises_exception_on_use(self):
        msg = (
            "django-testdata should not be used on Django 3.2, since it has "
            + "been merged into Django core."
        )
        with self.assertRaisesMessage(TypeError, msg):
            @wrap_testdata
            def example():
                pass
