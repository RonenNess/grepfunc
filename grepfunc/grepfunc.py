#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provide a unix-like grep function for Python.

Author: Ronen Ness.
Since: 2017.
"""
import re

# get python base string for either Python 2.x or 3.x
try:
    _basestring = basestring
except NameError:
    _basestring = str


def grep(target, pattern, **kwargs):
    """
    Main grep function
    :param target: Target to apply grep on. Can be a single string, an iterable, or an opened file handler.
    :param pattern: Grep pattern to search.
    :param kwargs: Optional flags (note: the docs below talk about matching 'lines', but this function also accept lists
                    and other iterables - in those cases, a 'line' means a single value from the iterable).

        The available flags are:

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

    :return: A list with matching lines (even if provided target is a single string), unless flags state otherwise.
    """
    # unify flags (convert shortcuts to full name)
    kwargs.setdefault('fixed_strings', kwargs.get('F'))
    kwargs.setdefault('basic_regexp', kwargs.get('G'))
    kwargs.setdefault('extended_regexp', kwargs.get('E'))
    kwargs.setdefault('ignore_case', kwargs.get('i'))
    kwargs.setdefault('invert', kwargs.get('v'))
    kwargs.setdefault('words', kwargs.get('w'))
    kwargs.setdefault('line', kwargs.get('x'))
    kwargs.setdefault('count', kwargs.get('c'))
    kwargs.setdefault('max_count', kwargs.get('m'))
    kwargs.setdefault('quiet', kwargs.get('q'))
    kwargs.setdefault('offset', kwargs.get('o'))
    kwargs.setdefault('line_number', kwargs.get('n'))
    kwargs.setdefault('regex_flags', kwargs.get('r'))
    kwargs.setdefault('keep_eol', kwargs.get('k'))

    # parse the params that are relevant to this function
    f_count = kwargs.get('count')
    f_max_count = kwargs.get('max_count')
    f_quiet = kwargs.get('quiet')
    f_offset = kwargs.get('offset')
    f_line_number = kwargs.get('line_number')
    f_trim = kwargs.get('trim')

    # if we got a single string convert it to a list
    if isinstance(target, _basestring):
        target = [target]

    # calculate if need to trim end of lines
    need_to_trim_eol = not kwargs.get('keep_eol') and hasattr(target, 'readline')

    # iterate target and grep
    ret = []
    for line_index, line in enumerate(target):

        # trim end of line
        if need_to_trim_eol and line.endswith('\n'):
            line = line[:-1]

        # check if need to trim all values
        if f_trim:
            line = line.trim()

        # do grap
        match, index = __do_grep(line, pattern, **kwargs)

        # if matched
        if match:

            # if quiet mode no need to continue, just return True
            if f_quiet:
                return True

            # if requested offset, add offset + line to return list
            if f_offset:
                ret.append((index, line))

            # if requested line number, add offset + line to return list
            elif f_line_number:
                ret.append((index, line_index))

            # default: add line to return list
            else:
                ret.append(line)

            # if have max limit and exceeded that limit, break:
            if f_max_count and len(ret) > f_max_count:
                break

    # if quiet mode and got here it means we didn't find a match
    if f_quiet:
        return False

    # if requested count return results count
    if f_count:
        return len(ret)

    # return results list
    return ret


def __do_grep(curr_line, pattern, **kwargs):
    """
    Do grep on a single string.
    See 'grep' docs for info about kwargs.
    :param curr_line: a single line to test.
    :param pattern: pattern to search.
    :return: (matched, position).
    """
    # currently found position
    position = -1

    # check if fixed strings mode
    if kwargs.get('fixed_strings'):

        # if case insensitive fix case
        if kwargs.get('ignore_case'):
            pattern = pattern.lower()
            curr_line = curr_line.lower()

        # split string patterns and iterate them
        patterns = pattern.split('\n')
        for p in patterns:

            # test current string
            position = curr_line.find(p)

            # found? break
            if position != -1:
                break

        # check if need to match whole words
        if kwargs.get('words') and position != -1:

            # first validate starting position
            if position != 0 and curr_line[position].isalpha() and curr_line[position] != '_':
                position = -1

    # if not fixed string, it means its a regex
    else:

        # set regex flags
        flags = kwargs.get('regex_flags') or 0
        flags |= re.IGNORECASE if kwargs.get('ignore_case') else 0

        # add whole-words option
        if kwargs.get('words'):
            pattern = r'\b' + pattern + r'\b'

        # do search
        result = re.search(pattern, curr_line, flags)

        # if found, set position
        if result:
            position = result.start()

    # check if need to match whole line
    if kwargs.get('line') and position != len(curr_line):
        position = -1

    # parse return value
    matched = position != -1

    # if invert flag is on, invert value
    if kwargs.get('invert'):
        matched = not matched

    # return result
    return matched, position
