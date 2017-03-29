#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the file filters.
"""
from grepfunc import grep
import unittest

"""
chubby
hub
Hub
dog
hottub
blue hub
green HuB.
"""

class TestGrep(unittest.TestCase):
    """
    Unittests to test grep.
    """
    # test file path
    test_file_path = "test.txt"

    # test words (read from file)
    with open(test_file_path, 'r') as infile:
        test_words = [x.strip() for x in infile.readlines()]

    @property
    def test_file(self):
        """
        get opened test file.
        """
        return open(self.test_file_path, 'r')

    @property
    def test_list(self):
        """
        get test list of words.
        """
        return self.test_words[:]

    def test_basic(self):
        """
        Testing creation of a basic filter.
        """
        self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(self.test_list, "hub"))
