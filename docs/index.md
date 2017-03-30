# GrepFunc
Simple grep-like function for Python.

Source at [GitHub](https://github.com/RonenNess/grepfunc).
Docs at [PythonHosted.org](http://pythonhosted.org/grepfunc/).

## Install

Install GrepFunc via pip:

```python
pip install grepfunc
```

## How to use

```GrepFunc``` provide a single function, ```grep```, which imitates Unix's ```grep``` functionality, but operate on lists and variables instead of files.

The function accept a single string, an iterable, or an opened file handler to search. The default return value is a list of matching strings from input.

### Flags

```GrepFunc``` comes with a set of flags you can set to change ```grep```'s behavior (implemented as named arguments).

The flags try to imitate the Unix ```grep``` flags as much as possible, but obviously since we are dealing with variables and not files, some flags were omitted / changed.

The following flags are currently supported:

```
    # unix grep imitating flags:
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

    # non standard flags
    - r, regex_flags:        Any additional regex flags you want to add when using regex (see python re flags).
    - k, keep_eol            When iterating file, if this option is set will keep the end-of-line at the end of every
                             line. If not (default) will trim the end of line character.
    - t, trim                Trim all whitespace characters from every line processed.

```

### Usage examples

The following is a set of examples to show how to use ```GrepFunc```.

#### Simple grep

The following example will return a list of movie names with the word 'dog' in them.

```python
from grepfunc import grep

movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']

# grep titles with the word 'dog' in them. Note: i=True will ignore case.
grep(movies, "dog", i=True)

# output:
# >>> ['Ghost Dog', 'Cats and Dogs', 'Reservoir Dogs']
```

#### Invert grep

The following example will return a list of movie names without the word 'dog' in them.

```python
from grepfunc import grep

movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']

# grep titles *without* the word 'dog' in them. Note: i=True will ignore case.
grep(movies, "dog", i=True, v=True)

# output:
# >>> ['Die Hard', 'Matrix', 'The Ring', 'Batman', 'Superman']
```

#### Grep on file

The following example will return a list of movie names without the word 'dog' in them, read from a file.

```python
from grepfunc import grep

# the file contains the following list of words: ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']
infile = open('movies.txt', 'r')

# grep titles *without* the word 'dog' in them from file. Note: i=True will ignore case.
grep(infile, "dog", i=True)

# output:
# >>> ['Ghost Dog', 'Cats and Dogs', 'Reservoir Dogs']
```

#### Quiet grep

The following example Will return True if the list contains a movie title with the word 'dog'.

```python
from grepfunc import grep

movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']

# grep if the word 'dog' appears in any of the movie titles. Note: set i=True to ignore case.
grep(movies, "dog", i=True, q=True)

# output:
# >>> True
```

### Iterator

Sometimes you need to scan a really large file, or an endless source of input (like an open socket etc). To handle those cases, you can use the alternative ```grep_iter``` function:

```python
from grepfunc import grep_iter

# a really large file that contain the names of all people in the world
infile = open('all_people_in_the_world.txt', 'r')

# print all people with first name 'Bob'
for person in grep_iter(infile, "^Bob\s"):
    print person
```

```grep_iter``` works just like ```grep```, but will return a memory efficient iterator instead of a list.

## Run Tests

From ```GrepFunc``` root dir:

```shell
cd tests
python test_all.py
```

Note that the tests are not included in the pypi package, so to run them please clone the git repository from [GitHub](https://github.com/RonenNess/grepfunc).

## Changes

.

## Contact

For bugs please use [GitHub issues](https://github.com/RonenNess/grepfunc/issues).
For other matters feel free to contact me at ronenness@gmail.com.

