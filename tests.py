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
from validol2 import validate, sequence, boolean, in_range, optional, ValidationError



class TestSimple(unittest.TestCase):
    def test_types(self):
        self.assertEqual(validate(str, "foo"), "foo")
        self.assertEqual(validate(str, 10), "10")
        self.assertEqual(validate(int, 10), 10)
        self.assertEqual(validate(int, "10"), 10)


class TestExtensions(unittest.TestCase):
    def test_sequence(self):
        self.assertEqual(validate(sequence([int]), ["10"]), [10])
        self.assertEqual(validate(sequence([0, 1, 2, 3]), [0, 1, 2, 3]), [0, 1, 2, 3])
        self.assertEqual(validate(sequence((bool, str)), (True, "Foo")), (True, "Foo"))

    def test_boolean(self):
        self.assertEqual(validate(boolean, 0), False)
        self.assertEqual(validate(boolean, 1), True)
        self.assertEqual(validate(boolean, "False"), False)
        self.assertEqual(validate(boolean, "True"), True)

    def test_in_range(self):
        self.assertEqual(validate(in_range(0, 5), 3), 3)

class TestDict(unittest.TestCase):
    def test_optional(self):
        self.assertEqual(validate({"email": str,
                                   "blocked": boolean,
                                    optional("interests"): sequence([str])},
                                  {"email": "john@example.com",
                                   "blocked": False,
                                   "interests": ["fishing", "cooking"]}),
                         {"email": "john@example.com",
                          "blocked": False,
                          "interests": ["fishing", "cooking"]})


if __name__ == '__main__':
    unittest.main()