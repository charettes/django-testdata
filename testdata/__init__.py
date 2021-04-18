from .descriptors import testdata
from .decorators import wrap_testdata

import django.utils.version

__all__ = ['VERSION', '__version__', 'testdata', 'wrap_testdata']

VERSION = (1, 0, 3, 'final', 0)

__version__ = django.utils.version.get_version(VERSION)
