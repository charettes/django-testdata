from __future__ import unicode_literals

from django.db import models

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    def python_2_unicode_compatible(cls):
        return cls


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
