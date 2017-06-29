# -*- encoding: utf-8 -*-

import unittest
import sys
import os.path

# need to go one more level up to load like Sublime Text Does 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from YAMLKeymap.to_keymap import format_context as original_format_context

def format_context(string):
    keybinding = {
        'context': [string]
    }
    original_format_context(keybinding)
    return keybinding['context'][0]

class TestContext(unittest.TestCase):
    
    def test_equal(self):
        self.assertEqual(format_context('key == operand'), {"key": "key", "operand": "operand"})
        self.assertEqual(format_context('key ==@ operand'), {"key": "key", "operand": "operand", "match_all": True})

    def test_unequal(self):
        self.assertEqual(format_context('key != operand'), {"key": "key", "operator": "not_equal", "operand": "operand"})
        self.assertEqual(format_context('key !=@ operand'), {"key": "key", "operator": "not_equal", "operand": "operand", "match_all": True})

    def test_key_alone(self):
        self.assertEqual(format_context('key'), {"key": "key"})

if __name__ == '__main__':
    unittest.main()