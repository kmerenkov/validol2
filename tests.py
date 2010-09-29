#!/usr/bin/env python

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2010 Konstantin Merenkov <kmerenkov@gmail.com>
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.


__author__  = "Konstantin Merenkov <kmerenkov@gmail.com>"


import unittest
import re
from itertools import cycle
from validol2 import *


class TestSimple(unittest.TestCase):
    def test_types(self):
        self.assertEqual(validate(str, "foo"), "foo")
        self.assertEqual(validate(str, 10), "10")
        self.assertEqual(validate(int, 10), 10)
        self.assertEqual(validate(int, "10"), 10)


class TestExtensions(unittest.TestCase):
    def test_sequence(self):
        self.assertEqual(validate([int], ["10"]), [10])
        self.assertEqual(validate(cycle([0, 1, 2, 3]), [0, 1, 2, 3]), [0, 1, 2, 3])
        self.assertEqual(validate(cycle((bool, str)), (True, "Foo")), (True, "Foo"))
        self.assertEqual(validate(set([1, 2, 3]), set([3, 2, 1])), set([2, 1, 3]))

    def test_nums(self):
        self.assertEqual(validate(gt(0), 10), 10)
        self.assertEqual(validate(lt(0), -10), -10)

    def test_boolean(self):
        self.assertEqual(validate(boolean, 0), False)
        self.assertEqual(validate(boolean, 1), True)
        self.assertEqual(validate(boolean, "False"), False)
        self.assertEqual(validate(boolean, "True"), True)

    def test_in_range(self):
        self.assertEqual(validate(in_range(0, 5), 3), 3)

    def test_regexp(self):
        r = re.compile('.*FOO.*')
        self.assertEqual(validate(regexp(r), 'barFOObar'), 'barFOObar')


class TestDict(unittest.TestCase):
    def test_optional(self):
        self.assertEqual(validate({"email": str,
                                   "blocked": boolean,
                                    optional("interests"): cycle([str])},
                                  {"email": "john@example.com",
                                   "blocked": False,
                                   "interests": ["fishing", "cooking"]}),
                         {"email": "john@example.com",
                          "blocked": False,
                          "interests": ["fishing", "cooking"]})

    def test_bug_dict_scheme_detection_works_improperly(self):
        try:
            self.assertRaises(ValidationError,
                              validate, {'foo': 'bar'}, [1])
        except Exception as e:
            msg = 'ValidationError was not raised, got %s instead: %s'
            self.fail(msg % (e.__class__.__name__, e, ))


if __name__ == '__main__':
    unittest.main()
