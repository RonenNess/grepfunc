#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the file filters.
"""
from grepfunc import grep, grep_iter
import unittest

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
        Testing basic grep with regex and fixed strings.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub"))
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub", F=True))
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, ["hub"], F=True))
            self.assertListEqual(['chubby', 'hub', 'dog', 'blue hub'], grep(source, ["hub", "dog"], F=True))

    def test_regex(self):
        """
        Testing a simple regex expression.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "h.b"))

    def test_grep_iter(self):
        """
        Testing grep_iter with no special flags.
        """
        for title, source in self.get_sources():

            ret = []
            for i in grep_iter(source, "hub"):
                ret.append(i)
            self.assertListEqual(['chubby', 'hub', 'blue hub'], ret)

            ret = []
            for i in grep_iter(source, "hub", F=True):
                ret.append(i)
            self.assertListEqual(['chubby', 'hub', 'blue hub'], ret)

    def test_case_insensitive(self):
        """
        Testing case insensitive flags.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['chubby', 'hub', 'Hub', 'green HuB.', 'blue hub'], grep(source, "hub", i=True))
            self.assertListEqual(['chubby', 'hub', 'Hub', 'green HuB.', 'blue hub'], grep(source, "hub", i=True, F=True))

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
            self.assertEqual(4, grep(source, "h", c=True))
            self.assertEqual(6, grep(source, "h", c=True, i=True))

    def test_max_count(self):
        """
        Testing max count flag.
        """
        for title, source in self.get_sources():
            self.assertEqual(2, grep(source, "h", c=True, m=2))
            self.assertEqual(2, grep(source, "h", c=True, m=2, i=True))

    def test_quiet(self):
        """
        Testing quiet flag.
        """
        for title, source in self.get_sources():
            self.assertEqual(True, grep(source, "hub", c=True, q=True))
            self.assertEqual(True, grep(source, "hub", c=True, q=True, i=True))
            self.assertEqual(True, grep(source, "dog", c=True, q=True, i=True))
            self.assertEqual(False, grep(source, "wrong", c=True, q=True, i=True))

    def test_offset(self):
        """
        Testing offset flag.
        """
        for title, source in self.get_sources():
            self.assertListEqual([(1, 'chubby'), (0, 'hub'), (5, 'blue hub')], grep(source, "hub", b=True))

    def test_only_match(self):
        """
        Testing only_match flag.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['hub', 'hub', 'Hub', 'HuB', 'hub'], grep(source, "hub", o=True, i=True))

    def test_line_number(self):
        """
        Testing line number flag.
        """
        for title, source in self.get_sources():
            self.assertListEqual([(0, 'chubby'), (1, 'hub'), (6, 'blue hub')], grep(source, "hub", n=True))

    def test_keep_eol(self):
        """
        Testing keep eol flag.
        """
        self.assertListEqual(['chubby\n', 'hub\n', 'blue hub\n'], grep(self.test_file, "hub", k=True))
        self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(self.test_list, "hub", k=True))

    def test_trim(self):
        """
        Testing trim flag.
        """
        for title, source in self.get_sources():
            self.assertListEqual(['hottub'], grep(source, "hottub", t=True))

    def test_re_flags(self):
        """
        Testing re-flags flags.
        """
        import re
        for title, source in self.get_sources():

            # test re flag ignore case. note: in second call the flag is ignored because we use pattern as strings.
            self.assertListEqual(['chubby', 'hub', 'Hub', 'green HuB.', 'blue hub'], grep(source, "hub", r=re.IGNORECASE))
            self.assertListEqual(['chubby', 'hub', 'blue hub'], grep(source, "hub", r=re.IGNORECASE, F=True))

    def test_after_context(self):
        """
        Testing after context flag.
        """
        # test after-context alone
        for title, source in self.get_sources():
            self.assertListEqual([['dog', 'hottub', 'green HuB.']], grep(source, "dog", A=2, t=True))
            self.assertListEqual([['blue hub']], grep(source, "blue hub", A=2, t=True))

        # combined with before-context
        for title, source in self.get_sources():
            self.assertListEqual([['Hub', 'dog', 'hottub', 'green HuB.']], grep(source, "dog", A=2, B=1, t=True))

    def test_before_context(self):
        """
        Testing before context flag.
        """
        # test before-context alone
        for title, source in self.get_sources():
            self.assertListEqual([['hub', 'Hub', 'dog']], grep(source, "dog", B=2, t=True))
            self.assertListEqual([['chubby']], grep(source, "chubby", B=2, t=True))

        # combined with after-context
        for title, source in self.get_sources():
            self.assertListEqual([['hub', 'Hub', 'dog', 'hottub  ']], grep(source, "dog", B=2, A=1))
