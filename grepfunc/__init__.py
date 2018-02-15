#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = ['grep', 'grep_iter', ]

__title__ = 'grepfunc'
__version__ = '1.0.1'
__author__ = 'Ronen Ness'
__license__ = 'MIT'

from . import grepfunc as _grepfunc
grep = _grepfunc.grep
grep_iter = _grepfunc.grep_iter

