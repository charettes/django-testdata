from __future__ import unicode_literals

import copy


class testdata(object):
    """
    Descriptor meant to provide TestCase instance isolation for attributes
    assigned during the setUpTestData phase.

    It allows the manipulation of objects assigned in setUpTestData by test
    methods without having to ensure the data is refetched from the database
    """
    memo_attr = '_testdata_memo'

    def __init__(self, data, name=None):
        self.data = data
        self.name = name

    def get_memo(self, testcase):
        try:
            memo = getattr(testcase, self.memo_attr)
        except AttributeError:
            memo = {}
            setattr(testcase, self.memo_attr, memo)
            testcase.addCleanup(delattr, testcase, self.memo_attr)
        return memo

    def __get__(self, instance, owner):
        if instance is None:
            return self.data

        memo = self.get_memo(instance)
        try:
            data = copy.deepcopy(self.data, memo)
        except TypeError:
            if self.name is not None:
                raise TypeError(
                    "%s.%s.%s must be deepcopy'able to be wrapped in testdata." % (
                        owner.__module__,
                        owner.__name__,
                        self.name,
                    )
                )
            raise TypeError(
                "%r must be deepcopy'able to be wrapped in testdata." % self.data
            )
        if self.name is not None:
            setattr(instance, self.name, data)
            # Avoid keeping a reference to cached attributes on teardown as it
            # prevents garbage collection of objects until the suite collected.
            instance.addCleanup(delattr, instance, self.name)
        return data
