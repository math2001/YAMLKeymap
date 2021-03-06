# -*- encoding: utf-8 -*-

"""
These tests are global, they migth not check every little things.

To run them, just run this file (ctrl+b by default)
"""

import unittest
import sys
import os.path

# need to go one more level up to load like Sublime Text Does 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from YAMLKeymap.api import to_keymap

TEST_SEPARATOR = '\n---!---\n'
TEST_RESULT_SEPARATOR = '>>>>>>\n'

class Global(unittest.TestCase):

    def run_test_from_file(self, file):
        with open(file, encoding='utf-8') as fp:
            tests = fp.read().split(TEST_SEPARATOR)

        for test in tests:
            original, result = test.split(TEST_RESULT_SEPARATOR)
            self.assertEqual(to_keymap(original, dumper='custom'), result) 

    def test_simples(self):
        self.run_test_from_file('simples.txt')

    def test_with_args(self):
        self.run_test_from_file('with-args.txt')

    def test_with_context(self):
        self.run_test_from_file('with-context.txt')

if __name__ == '__main__':
    unittest.main()