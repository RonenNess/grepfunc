# GrepFunc
Lightweight lib to iterate and process files using multiple sources and filters.

Source at [GitHub](https://github.com/RonenNess/grepfunc).
Docs at [PythonHosted.org](http://pythonhosted.org/grepfunc/).

## Install

Install grepfunc via pip:

```python
pip install grepfunc
```

## How to use

GrepFunc provide a single function, grep, which works pretty much like the Unix's grep command but implemented as a Python function and operates on variables.

```grep``` can accept a single string, an iterable, or an opened file. Its default return value is a list of matching strings from input.

### Flags

When using ```grep``` you can set different flags (implemented as named arguments).
GrepFunc tries to imitate the Unix ```grep``` command flags, but obviously since we are not dealing with files here many flags were omitted.

GrepFunc support the following flags:

```
    unix grep standard flags:

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

    non standard flags:

    - r, regex_flags:       Any additional regex flags you want to add when using regex (see python re flags).
    - k, keep_eol           When iterating file, if this option is set will keep the end-of-line at the end of every
                            line. If not (default) will trim the end of line character.
    - t, trim               If true, will trim all whitespace characters from every line processed
```

### Usage examples

The following is a set of examples to show how to use GrepFunc:

#### Simple grep

The following example Will return a list of movie names with the word 'dog' in them.

```python
from grepfunc import grep

# grep titles with the word 'dog' in them. Note: set i=True to ignore case.
movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']
print "Movies with 'Dog' in the title", grep(movies, "dog", i=True)

# output:
# >>> Movies with 'Dog' in the title ['Ghost Dog', 'Cats and Dogs', 'Reservoir Dogs']
```

#### Invert grep

The following example Will return a list of movie names without the word 'dog' in them.

```python
from grepfunc import grep

# grep titles with the word 'dog' in them. Note: set i=True to ignore case.
movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']
print "Movies without 'Dog' in the title", grep(movies, "dog", i=True, v=True)

# output:
# >>> Movies without 'Dog' in the title ['Die Hard', 'Matrix', 'The Ring', 'Batman', 'Superman']
```

#### Grep on file

The following example Will return a list of movie names without the word 'dog' in them, read from a file.

```python
from grepfunc import grep

# grep titles with the word 'dog' in them. Note: set i=True to ignore case.
infile = open('movies.txt', 'r')
print "Movies without 'Dog' in the title", grep(infile, "dog", i=True, v=True)

# output:
# >>> Movies with 'Dog' in the title ['Ghost Dog', 'Cats and Dogs', 'Reservoir Dogs']
```

#### Quiet grep

The following example Will return True if the list contains a movie title with the word 'dog'.

```python
from grepfunc import grep

# grep titles with the word 'dog' in them. Note: set i=True to ignore case.
movies = ['Ghost Dog', 'Die Hard', 'Matrix', 'The Ring', 'Cats and Dogs', 'Batman', 'Superman', 'Reservoir Dogs']
print "Got a movie with 'Dog' in title?", grep(movies, "dog", i=True, q=True)

# output:
# >>> Got a movie with 'Dog' in title? True
```

## Run Tests

From GrepFunc root dir:

```shell
cd tests
python test_all.py
```

Tests are not included in the pypi package, to run them please clone from git.

## Changes

## Contact

For bugs please use [GitHub issues](https://github.com/RonenNess/grepfunc/issues).
For other matters feel free to contact me at ronenness@gmail.com.

