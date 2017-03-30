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

flags:
    - F, fixed_strings:     Interpret 'pattern' as a list of fixed strings, separated by newlines, any of which is
                            to be matched. If not set, will interpret 'pattern' as a python regular expression.
    - i, ignore_case:       Ignore case.
    - v, invert:            Invert (eg return non-matching lines / values).
    - w, words:             Select only those lines containing matches that form whole words.
    - x, line:              Select only matches that exactly match the whole line.
    - c, count:             Instead of the normal output, print a count of matching lines.
    TBD- m NUM, max_count:     Stop reading after NUM matching values.
    TBD- q, quiet:             Instead of returning string / list of strings return just a single True / False if
                            found matches.
    TBD- o, offset:            Instead of a list of strings will return a list of (offset, string), where offset is
                            the offset of the matched 'pattern' in line.
    TBD- n, line_number:       Instead of a list of strings will return a list of (index, string), where index is the
                            line number.
    TBD- r, regex_flags:       Any additional regex flags you want to add when using regex (see python re flags).
    TBD- k, keep_eol           When iterating file, if this option is set will keep the end-of-line at the end of every
                            line. If not (default) will trim the end of line character.
    TBD- t, trim               If true, will trim all whitespace characters from every line processed.
"""

# test file path
test_file_path = "test.txt"


def _open_test_file():
    return open(test_file_path, 'r')


class TestGrep(unittest.TestCase):
    """
    Unittests to test grep.
    """
    # test words (read from file)
    with open(test_file_path, 'r') as infile:
        test_words = [x[:-1] for x in infile.readlines()]

    @property
    def test_file(self):
        """
        Get opened test file.
        Note: return a function and not a file instance so it will reopen it every call.
        """
        return _open_test_file

    @property
    def test_list(self):
        """
        Get test list of words.
        """
        return self.test_words[:]

    def get_sources(self):
        """
        Get list of titles and sources.
        """
        return [("file", self.test_file), ("list", self.test_list)]

    def test_basic(self):
        """
        Testing basic grep with no special flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub"))
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub", F=True))

    def test_case_insensitive(self):
        """
        Testing case insensitive flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'Hub', 'blue hub', 'green HuB.'], grep(source, "hub", i=True))
            self.assertListEqual(['chubby', 'hub', 'Hub', 'blue hub', 'green HuB.'], grep(source, "hub", i=True, F=True))

    def test_invert(self):
        """
        Testing invert flags.
        """
        for title, source in self.get_sources():

            # check invert
            self.assertListEqual(['Hub', 'dog', 'hottub  ', 'green HuB.'], grep(source, "hub", v=True))
            self.assertListEqual(['Hub', 'dog', 'hottub  ', 'green HuB.'], grep(source, "hub", v=True, F=True))

            # check invert with case insensitive as well
            self.assertListEqual(['dog', 'hottub  '], grep(source, "hub", i=True, v=True))
            self.assertListEqual(['dog', 'hottub  '], grep(source, "hub", i=True, v=True, F=True))

    def test_whole_words(self):
        """
        Testing whole words flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['hub', 'blue hub'], grep(source, "hub", w=True))
            self.assertListEqual(['hub', 'blue hub'], grep(source, "hub", w=True, F=True))

    def test_whole_lines(self):
        """
        Testing whole lines flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['hub'], grep(source, "hub", x=True))
            self.assertListEqual(['hub'], grep(source, "hub", x=True, F=True))

    def test_count(self):
        """
        Testing count flag.
        """
        for title, source in self.get_sources():
            self.assertEqual(3, grep(source, "hub", c=True))
            self.assertEqual(3, grep(source, "hub", c=True))
