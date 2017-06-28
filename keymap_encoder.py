# -*- encoding: utf-8 -*-

"""
Converts a python object into a JSON string, properly indented for sublime keymap
"""

import json

JSONEncoder = json.JSONEncoder(ensure_ascii=False)

class KeymapEncoder:

    def __init__(self, keymap):
        self.keymap = keymap
        self.lines = []
        self.indentation_level = 0
        self.indentation = '  '

    def add_line(self, *strings):
        self.lines.append((self.indentation * self.indentation_level) + ''.join(strings))

    def encode(self):

        self.add_line('[')
        self.indentation_level += 1

        for i, keybinding in enumerate(self.keymap):
            self.add_line('{')
            self.indentation_level += 1
            self.add_line('"keys": {},'.format(JSONEncoder.encode(keybinding['keys'])))
            self.add_line('"command": {}'.format(JSONEncoder.encode(keybinding['command'])))

            if 'args' in keybinding:
                self.lines[-1] += ','
                self.add_line('"args": {')
                self.indentation_level += 1
                for j, (key, value) in enumerate(keybinding['args'].items()):
                    self.add_line('{}: {}{}'.format(JSONEncoder.encode(key),
                                                    JSONEncoder.encode(value),
                                                    ',' if j + 1 < len(keybinding['args']) else ''))
                self.indentation_level -= 1
                self.add_line('}')

            if 'context' in keybinding:
                self.lines[-1] += ','
                self.add_line('"context": [')
                self.indentation_level += 1
                for j, context in enumerate(keybinding['context']):
                    string = '{"key": ' + JSONEncoder.encode(context['key'])

                    if 'operator' in context:
                        string += ', "operator": ' + JSONEncoder.encode(context['operator'])

                    if 'operand' in context:
                        string += ', "operand": ' + JSONEncoder.encode(context['operand'])

                    if 'match_all' in context:
                        string += ', "match_all": ' + JSONEncoder.encode(context['match_all'])

                    self.add_line(string + '}' + (',' if j + 1 < len(keybinding['context']) else ''))

                self.indentation_level -= 1
                self.add_line(']')

            self.indentation_level -= 1
            self.add_line('}' + (',' if i + 1 < len(self.keymap) else ''))

        self.indentation_level -= 1
        self.add_line(']')
        return '\n'.join(self.lines)

def keymap_encode(keymap):
    return KeymapEncoder(keymap).encode()

ORIGINAL_OBJECT = [
    {"keys": ["backspace"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Left Right.sublime-macro"},
        "context": [
            { "key": "selection_empty", "match_all": True },
            { "key": "following_text", "operator": "regex_contains", "operand": "^ \\}" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "\\{ $" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Left Right.sublime-macro"},
        "context": [
            { "key": "selector", "operator": "equal", "operand": "comment.block.documentation.python" },
            { "key": "selection_empty", "match_all": True },
            { "key": "following_text", "operator": "regex_contains", "operand": "^ \"\"\"" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "\"\"\" $" }
        ]
    },
    { "keys": ["}"], "command": "run_macro_file", "args": { "file": "Packages/User/macros/move-multi-blank-and-move-left.sublime-macro" },
    "context": [
        { "key": "following_text", "operator": "regex_contains", "operand": "^\\s+\\}" }
    ] },
]
