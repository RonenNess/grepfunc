#!/usr/bin/python
# -*- coding: utf-8 -*-

# to make the imports work in tests
if __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    print (path.dirname(path.dirname(path.abspath(__file__))))

# import all tests
from test_grepfunc import *

# run tests
if __name__ == '__main__':
    unittest.main()
