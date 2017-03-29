#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the file filters.
"""
from grepfunc import grep
import unittest

"""
words:

    chubby
    hub
    Hub
    dog
    hottub
    blue hub
    green HuB.
"""

"""
flags:

    - F, fixed_strings:     Interpret 'pattern' as a list of fixed strings, separated by newlines, any of which is
                            to be matched. If not set, will interpret 'pattern' as a python regular expression.
    - i, ignore_case:       Ignore case.
    - v, invert:            Invert (eg return non-matching lines / values).
    - w, words:             Select only those lines containing matches that form whole words.
    - x, line:              Select only matches that exactly match the whole line.
    - c, count:             Instead of the normal output, print a count of matching lines.
    - m NUM, max_count:     Stop reading after NUM matching values.
    - q, quiet:             Instead of returning string / list of strings return just a single True / False if
                            found matches.
    - o, offset:            Instead of a list of strings will return a list of (offset, string), where offset is
                            the offset of the matched 'pattern' in line.
    - n, line_number:       Instead of a list of strings will return a list of (index, string), where index is the
                            line number.
    - r, regex_flags:       Any additional regex flags you want to add when using regex (see python re flags).
    - k, keep_eol           When iterating file, if this option is set will keep the end-of-line at the end of every
                            line. If not (default) will trim the end of line character.
    - t, trim               If true, will trim all whitespace characters from every line processed.
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

    def get_sources(self):
        """
        get list of titles and sources.
        """
        return [("file", self.test_file), (self.test_list, "list")]

    def test_basic(self):
        """
        Testing creation of a basic filter.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub"), "Failed regular grep on " + title)
            self.assertListEqual(['chubby', 'hub', 'Hub', 'blue hub', 'green HuB.'], grep(source, "hub", F=True), "Failed regular grep with strings on " + title)

    def test_case_insensitive(self):
        """
        testing case insensitive flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'Hub', 'blue hub', 'green HuB.'], grep(source, "hub", i=True), "Failed insensitive grep on " + title)
            self.assertListEqual(['chubby', 'hub', 'Hub', 'blue hub', 'green HuB.'], grep(source, "hub", i=True, F=True), "Failed insensitive grep with strings on " + title)
