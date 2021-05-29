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

import os
import sqlite3

class KeyVal():
    def __init__(self, filename):
        self._filename = filename
        if not os.path.exists(filename):
            self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self._filename)
        cursor = conn.cursor()
        sql = 'DROP TABLE IF EXISTS keyval'
        cursor.execute(sql)
        conn.commit()
        sql = '''
            CREATE TABLE IF NOT EXISTS keyval(
            key TEXT,
            value TEXT,
            UNIQUE(key));
            '''
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def get(self, key):
        sql = "SELECT value FROM keyval WHERE key='{}'".format(key)
        conn = sqlite3.connect(self._filename)
        cursor = conn.cursor()
        cursor.execute(sql)
        ans = cursor.fetchone()
        cursor.close()
        conn.close()
        return ans[0] if ans else ""

    def set(self, key, value):
        sql = """
            INSERT INTO keyval(key, value)
            VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value=excluded.value
            """
        conn = sqlite3.connect(self._filename)
        cursor = conn.cursor()
        cursor.execute(sql, (key, value))
        conn.commit()
        cursor.close()
        conn.close()
