#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Here is the test file for insuring the script under test functions
as expected.  It executes the script, removes varying characters (numbers)
from the html file produced, converts that to a SHA224 hash and applies
assertTrue method to the hash and the expected hash.  If the two are the
same, the script passes the test.

"""
import unittest
from fermilab_research_glance import create_table
import hashlib
import re

class ResearchGlanceTests(unittest.TestCase):
    """Set of unit tests for fermilab_research_glance.py."""
    def test_research_glance(self):
        """Compare expected output with actual output of
        fermilab_research_glance.py.

        """
        static_hash = '450832eaed17fdffb05210088921cbe913b854e9bb3f873de96475d2'
        test_run = re.sub(r'\d', r'', create_table())
        test_run_hash = hashlib.sha224(test_run).hexdigest()
        self.assertTrue(test_run_hash == static_hash, "Result does not match \
static hash")

if __name__ == '__main__':
    unittest.main()


