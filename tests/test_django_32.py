# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import SkipTest

import django
from django.test import SimpleTestCase

from testdata import wrap_testdata


class WrapTestDataTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        if django.VERSION < (3, 2):
            raise SkipTest("Django 3.2 only test.")

    def test_raises_exception_on_use(self):
        msg = (
            "django-testdata should not be used on Django 3.2, since it has "
            + "been merged into Django core."
        )
        with self.assertRaisesMessage(TypeError, msg):
            @wrap_testdata
            def example():
                pass
