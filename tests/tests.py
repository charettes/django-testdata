# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
from unittest import SkipTest

import django
from django.test import TestCase

from testdata import testdata, wrap_testdata

from .models import Author

if django.VERSION >= (3, 2):
    raise SkipTest("Django 3.2 includes functionality.")


class UnDeepCopyAble(object):
    def __repr__(self):
        return str('<UnDeepCopyAble object>')

    def __deepcopy__(self, memo):
        raise TypeError('Not deep copyable.')


def assert_no_queries(test):
    @wraps(test)
    def inner(self):
        with self.assertNumQueries(0):
            test(self)
    return inner


class TestDataTests(TestCase):
    wrapper = testdata
    undeepcopyable_message = (
        "<UnDeepCopyAble object> must be deepcopy'able to be wrapped in testdata."
    )

    @classmethod
    def setUpTestData(cls):
        cls.aldous = cls.wrapper(Author.objects.create(
            name='Aldous Huxley',
        ))
        cls.brave_new_world = cls.wrapper(cls.aldous.books.create(
            title='Brave New World',
        ))
        cls.books = cls.wrapper([
            cls.aldous.books.create(
                title='Chrome Yellow'
            ),
            cls.brave_new_world,
        ])
        cls.unpickleable = cls.wrapper(UnDeepCopyAble())

    @assert_no_queries
    def access_testdata(self):
        self.aldous

    @assert_no_queries
    def test_attributes_cleanup(self):
        """Attributes assigned during """
        test = TestDataTests('access_testdata')
        pre_attributes = set(test.__dict__)
        test.run()
        post_attributes = set(test.__dict__)
        self.assertEqual(pre_attributes, post_attributes)

    @assert_no_queries
    def test_class_attribute_equality(self):
        """Class level test data is equal to instance level test data."""
        self.assertEqual(self.aldous, self.__class__.aldous)

    @assert_no_queries
    def test_class_attribute_identity(self):
        """Class level test data is not identical to instance level test data."""
        self.assertIsNot(self.aldous, self.__class__.aldous)

    @assert_no_queries
    def test_identity_preservation(self):
        """Identity of test data is preserved between accesses."""
        self.assertIs(self.aldous, self.aldous)

    @assert_no_queries
    def test_known_related_objects_identity_preservation(self):
        """Known related objects identity is preserved."""
        self.assertIs(self.aldous, self.brave_new_world.author)

    @assert_no_queries
    def test_list_object(self):
        self.assertIs(self.books[0].author, self.aldous)
        self.assertIs(self.books[-1], self.brave_new_world)

    def test_undeepcopyable(self):
        with self.assertRaisesMessage(TypeError, self.undeepcopyable_message):
            self.unpickleable


class WrapTestDataTests(TestDataTests):
    undeepcopyable_message = (
        "tests.tests.WrapTestDataTests.unpickleable must be deepcopy'able to be wrapped in testdata."
    )

    @staticmethod
    def wrapper(wrapped):
        return wrapped

    @classmethod
    @wrap_testdata
    def setUpTestData(cls):
        super(WrapTestDataTests, cls).setUpTestData()

    @assert_no_queries
    def test_name_attribute_assignment(self):
        """Name assignment through testdata(name) allows dict caching."""
        self.assertNotIn('aldous', self.__dict__)
        self.aldous
        self.assertIn('aldous', self.__dict__)
        self.assertIs(self.__dict__['aldous'], self.aldous)


class IntegrationTests(TestCase):
    @classmethod
    @wrap_testdata
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            name='Milan Kundera',
        )
        cls.book = cls.author.books.create(
            title='Nesnesitelná lehkost bytí',
        )

    def test_book_name_english(self):
        self.assertEqual(self.book.title, 'Nesnesitelná lehkost bytí')
        self.book.title = 'The Unbearable Lightness of Being'
        self.book.save()

    def test_book_name_french(self):
        self.assertEqual(self.book.title, 'Nesnesitelná lehkost bytí')
        self.book.title = "L'Insoutenable Légèreté de l'être"
        self.book.save()
