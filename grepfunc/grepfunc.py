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


def __fix_args(kwargs):
    """
    Set all named arguments shortcuts and flags.
    """
    kwargs.setdefault('fixed_strings', kwargs.get('F'))
    kwargs.setdefault('basic_regexp', kwargs.get('G'))
    kwargs.setdefault('extended_regexp', kwargs.get('E'))
    kwargs.setdefault('ignore_case', kwargs.get('i'))
    kwargs.setdefault('invert', kwargs.get('v'))
    kwargs.setdefault('words', kwargs.get('w'))
    kwargs.setdefault('line', kwargs.get('x'))
    kwargs.setdefault('count', kwargs.get('c'))
    kwargs.setdefault('max_count', kwargs.get('m'))
    kwargs.setdefault('after_context', kwargs.get('A'))
    kwargs.setdefault('before_context', kwargs.get('B'))
    kwargs.setdefault('quiet', kwargs.get('q'))
    kwargs.setdefault('byte_offset', kwargs.get('b'))
    kwargs.setdefault('only_matching', kwargs.get('o'))
    kwargs.setdefault('line_number', kwargs.get('n'))
    kwargs.setdefault('regex_flags', kwargs.get('r'))
    kwargs.setdefault('keep_eol', kwargs.get('k'))
    kwargs.setdefault('trim', kwargs.get('t'))


def _is_part_of_word(c):
    """
    return if a given character is a part of a word, eg not a word breaker character
    """
    return c.isalpha() or c == '_'


def grep(target, pattern, **kwargs):
    """
    Main grep function.
    :param target: Target to apply grep on. Can be a single string, an iterable, a function, or an opened file handler.
    :param pattern: Grep pattern to search.
    :param kwargs: Optional flags (note: the docs below talk about matching 'lines', but this function also accept lists
                    and other iterables - in those cases, a 'line' means a single value from the iterable).

        The available flags are:

        - F, fixed_strings:      Interpret 'pattern' as a string or a list of strings, any of which is to be matched.
                                 If not set, will interpret 'pattern' as a python regular expression.
        - i, ignore_case:        Ignore case.
        - v, invert:             Invert (eg return non-matching lines / values).
        - w, words:              Select only those lines containing matches that form whole words.
        - x, line:               Select only matches that exactly match the whole line.
        - c, count:              Instead of the normal output, print a count of matching lines.
        - m NUM, max_count:      Stop reading after NUM matching values.
        - A NUM, after_context:  Return NUM lines of trailing context after matching lines. This will replace the string
                                 part of the reply to a list of strings. Note that in some input types this might skip
                                 following matches. For example, if the input is a file or a custom iterator.
        - B NUM, before_context: Return NUM lines of leading context before matching lines. This will replace the string
                                 part of the reply to a list of strings.
        - q, quiet:              Instead of returning string / list of strings return just a single True / False if
                                 found matches.
        - b, byte_offset:        Instead of a list of strings will return a list of (offset, string), where offset is
                                 the offset of the matched 'pattern' in line.
        - n, line_number:        Instead of a list of strings will return a list of (index, string), where index is the
                                 line number.
        - o, only_matching:      Return only the part of a matching line that matches 'pattern'.
        - r, regex_flags:        Any additional regex flags you want to add when using regex (see python re flags).
        - k, keep_eol            When iterating file, if this option is set will keep the end-of-line at the end of every
                                 line. If not (default) will trim the end of line character.
        - t, trim                Trim all whitespace characters from every line processed.

    :return: A list with matching lines (even if provided target is a single string), unless flags state otherwise.
    """
    # unify flags (convert shortcuts to full name)
    __fix_args(kwargs)

    # parse the params that are relevant to this function
    f_count = kwargs.get('count')
    f_max_count = kwargs.get('max_count')
    f_quiet = kwargs.get('quiet')

    # use the grep_iter to build the return list
    ret = []
    for value in grep_iter(target, pattern, **kwargs):

        # if quiet mode no need to continue, just return True because we got a value
        if f_quiet:
            return True

        # add current value to return list
        ret.append(value)

        # if have max limit and exceeded that limit, break:
        if f_max_count and len(ret) >= f_max_count:
            break

    # if quiet mode and got here it means we didn't find a match
    if f_quiet:
        return False

    # if requested count return results count
    if f_count:
        return len(ret)

    # return results list
    return ret


def grep_iter(target, pattern, **kwargs):
    """
    Main grep function, as a memory efficient iterator.
    Note: this function does not support the 'quiet' or 'count' flags.
    :param target: Target to apply grep on. Can be a single string, an iterable, a function, or an opened file handler.
    :param pattern: Grep pattern to search.
    :param kwargs: See grep() help for more info.
    :return: Next match.
    """
    # unify flags (convert shortcuts to full name)
    __fix_args(kwargs)

    # parse the params that are relevant to this function
    f_offset = kwargs.get('byte_offset')
    f_line_number = kwargs.get('line_number')
    f_trim = kwargs.get('trim')
    f_after_context = kwargs.get('after_context')
    f_before_context = kwargs.get('before_context')
    f_only_matching = kwargs.get('only_matching')

    # if target is a callable function, call it first to get value
    if callable(target):
        target = target()

    # if we got a single string convert it to a list
    if isinstance(target, _basestring):
        target = [target]

    # calculate if need to trim end of lines
    need_to_trim_eol = not kwargs.get('keep_eol') and hasattr(target, 'readline')

    # list of previous lines, used only when f_before_context is set
    prev_lines = []

    # iterate target and grep
    for line_index, line in enumerate(target):

        # fix current line
        line = __process_line(line, need_to_trim_eol, f_trim)

        # do grap
        match, offset, endpos = __do_grep(line, pattern, **kwargs)

        # nullify return value
        value = None

        # if matched
        if match:

            # the textual part we return in response
            ret_str = line

            # if only return matching
            if f_only_matching:
                ret_str = ret_str[offset:endpos]

            # if 'before_context' is set
            if f_before_context:

                # make ret_str be a list with previous lines
                ret_str = prev_lines + [ret_str]

            # if need to return X lines after trailing context
            if f_after_context:

                # convert return string to list (unless f_before_context is set, in which case its already a list)
                if not f_before_context:
                    ret_str = [ret_str]

                # iterate X lines to read after
                for i in range(f_after_context):

                    # if target got next or readline, use next()
                    # note: unfortunately due to python files next() implementation we can't use tell and seek to
                    # restore position and not skip next matches.
                    if hasattr(target, '__next__') or hasattr(target, 'readline'):
                        try:
                            val = next(target)
                        except StopIteration:
                            break

                    # if not, try to access next item based on index (for lists)
                    else:
                        try:
                            val = target[line_index+i+1]
                        except IndexError:
                            break

                    # add value to return string
                    ret_str.append(__process_line(val, need_to_trim_eol, f_trim))

            # if requested offset, add offset + line to return list
            if f_offset:
                value = (offset, ret_str)

            # if requested line number, add offset + line to return list
            elif f_line_number:
                value = (line_index, ret_str)

            # default: add line to return list
            else:
                value = ret_str

        # maintain a list of previous lines, if the before-context option is provided
        if f_before_context:
            prev_lines.append(line)
            if len(prev_lines) > f_before_context:
                prev_lines.pop(0)

        # if we had a match return current value
        if value is not None:
            yield value


def __process_line(line, strip_eol, strip):
    """
    process a single line value.
    """
    if strip:
        line = line.strip()
    elif strip_eol and line.endswith('\n'):
        line = line[:-1]
    return line


def __do_grep(curr_line, pattern, **kwargs):
    """
    Do grep on a single string.
    See 'grep' docs for info about kwargs.
    :param curr_line: a single line to test.
    :param pattern: pattern to search.
    :return: (matched, position, end_position).
    """
    # currently found position
    position = -1
    end_pos = -1

    # check if fixed strings mode
    if kwargs.get('fixed_strings'):

        # if case insensitive fix case
        if kwargs.get('ignore_case'):
            pattern = pattern.lower()
            curr_line = curr_line.lower()

        # if pattern is a single string, match it:
        pattern_len = 0
        if isinstance(pattern, _basestring):
            position = curr_line.find(pattern)
            pattern_len = len(pattern)

        # if not, treat it as a list of strings and match any
        else:
            for p in pattern:
                position = curr_line.find(p)
                pattern_len = len(p)
                if position != -1:
                    break

        # calc end position
        end_pos = position + pattern_len

        # check if need to match whole words
        if kwargs.get('words') and position != -1:

            foundpart = (' ' + curr_line + ' ')[position:position+len(pattern)+2]
            if _is_part_of_word(foundpart[0]):
                position = -1
            elif _is_part_of_word(foundpart[-1]):
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
            end_pos = result.end()

    # check if need to match whole line
    if kwargs.get('line') and (position != 0 or end_pos != len(curr_line)):
        position = -1

    # parse return value
    matched = position != -1

    # if invert flag is on, invert value
    if kwargs.get('invert'):
        matched = not matched

    # if position is -1 reset end pos as well
    if not matched:
        end_pos = -1

    # return result
    return matched, position, end_pos
