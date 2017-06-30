# -*- encoding: utf-8 -*-

YAML_EXTENSION = '.sublime-yaml-keymap'
JSON_EXTENSION = '.sublime-keymap'

try:
    import sublime
except ImportError:
    sublime = None

def get_settings():
    return sublime.load_settings('YAMLKeymap.sublime-settings')

def is_dev():
    if sublime:
        return get_settings().get('is_dev')
    else:
        return True

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

def log(*args, **kwargs):
    # CSW: ignore
    print('YAMLKeymap ]>', *args, **kwargs)

def error_to_string(message, error):
    return "Error: {} ({}: {})".format(message, error.__class__.__name__, error)
