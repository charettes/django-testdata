from __future__ import unicode_literals

from functools import wraps

import django

from .descriptors import testdata


def wrap_testdata(setup):
    """
    A setUpTestData decorator that wraps every class attribute assignment
    during the execution of its decorated method into testdata instances.
    """
    if django.VERSION >= (3, 2):
        raise TypeError(
            "django-testdata should not be used on Django 3.2, since it has "
            + "been merged into Django core."
        )

    @wraps(setup)
    def inner(cls):
        pre_attrs = set(cls.__dict__)
        setup(cls)
        added_attrs = set(cls.__dict__) - pre_attrs
        for attr in added_attrs:
            value = getattr(cls, attr)
            setattr(cls, attr, testdata(value, attr))
    return inner
