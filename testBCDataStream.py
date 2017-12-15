#!/usr/bin/env python3
#
# Copyright (c) 2010 Gavin Andresen
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Unit tests for BCDataStream class."""

import unittest

import BCDataStream

class Tests(unittest.TestCase):
  def setUp(self):
    self.ds = BCDataStream.BCDataStream()

  def testString(self):
    t = {
      "\x07setting" : "setting",
      "\xfd\x00\x07setting" : "setting",
      "\xfe\x00\x00\x00\x07setting" : "setting",
      }
    for (input, output) in t.iteritems():
      self.ds.clear()
      self.ds.write(input)
      got = self.ds.read_string()
      self.assertEqual(output, got)

if __name__ == "__main__":
  unittest.main()
