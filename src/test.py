#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

import os
from keyval import KeyVal

class TestDb(unittest.TestCase):
    def setUp(self):
        self._filename = 'test.db'
        if os.path.exists(self._filename):
            os.remove(self._filename)
        self._keyval = KeyVal(self._filename)

    def tearDown(self):
        if os.path.exists(self._filename):
            os.remove(self._filename)

    def test_new(self):
        self._keyval.set('key', 'val')
        val = self._keyval.get('key')
        self.assertEqual(val, 'val')

    def test_update(self):
        self._keyval.set('key', 'val')
        val = self._keyval.get('key')
        self.assertEqual(val, 'val')
        self._keyval.set('key', 'val2')
        val = self._keyval.get('key')
        self.assertEqual(val, 'val2')


if __name__ == '__main__':
    unittest.main()
