# -*- encoding: utf-8 -*-

YAML_EXTENSION = '.sublime-yaml-keymap'
JSON_EXTENSION = '.sublime-keymap'

class ConversionError(Exception):
    pass

CONTEXT_OPERATORS = {
    
    '==': 'equal',
    '!=': 'not_equal',
    '^==': 'regex_match',
    '^!=': 'not_regex_match',
    '*==': 'regex_contains',
    '*!=': 'not_regex_contains',

}

CONTEXT_OPERATORS_INVERSE = dict((v, k) for k, v in CONTEXT_OPERATORS.items())