#!/usr/bin/env python

import unittest

from pydarts.communication import (sanitized_input, SanitizationError,
        MinLargerMaxError, TestingCommunicator)


class SanitizedInputTestCase(unittest.TestCase):

    def test_min_larger_max(self):
        self.assertRaises(MinLargerMaxError, sanitized_input, "foo", min_=1,
                max_=0)

    def test_wrong_type(self):
        self.assertRaises(SanitizationError, sanitized_input, "foo", type_=int)

    def test_too_large(self):
        self.assertRaises(SanitizationError, sanitized_input, "42", type_=int,
                max_=11)

    def test_too_small(self):
        self.assertRaises(SanitizationError, sanitized_input, "42", type_=int,
                min_=1337)

    def test_too_short(self):
        self.assertRaises(SanitizationError, sanitized_input, "bar", min_=5)

    def test_valid_str(self):
        self.assertEqual(sanitized_input("süß", min_=1), "süß")

    def test_valid_int(self):
        self.assertEqual(sanitized_input("123", type_=int, max_=180), 123)

    def test_strip(self):
        self.assertEqual(sanitized_input(" 99  ", type_=str), "99")


class TestingCommunicatorTestCase(unittest.TestCase):
    def setUp(self):
        self.data = (11, "2d", 180, "0", "d", 33)
        self.communicator = TestingCommunicator(*self.data)

    def test_data(self):
        for i, d in enumerate(self.data):
            self.assertEqual(str(d), self.communicator._data[i])

    def test_get_input(self):
        self.assertEqual(str(self.data[0]), self.communicator.get_input())
        self.assertEqual(self.data[1], self.communicator.get_input())
        self.assertEqual(str(self.data[2]), self.communicator.get_input())

    def test_print_info(self):
        self.assertIsNone(self.communicator.print_info("some text"))

    def test_print_error(self):
        class TestException(Exception):
            pass
        self.assertRaises(TestException,
                          self.communicator.print_error, error=TestException())

    def test_get_typed_input(self):
        self.assertEqual(str(self.data[0]), self.communicator.get_input())
        self.assertEqual(self.data[1], self.communicator.get_input())
        self.assertEqual(self.data[2], self.communicator.get_input(type_=int))
        self.assertEqual(int(self.data[3]),
                self.communicator.get_input(type_=int))


if __name__ == "__main__":
    unittest.main()
