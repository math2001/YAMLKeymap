# -*- encoding: utf-8 -*-

# from .constants import *
import yaml

class YamlDumper:

    def __init__(self, keymap):
        self.keymap = keymap
        self.lines = []
        self.indentation_level = 0
        self.indentation = '  '

    def add_lines(self, *strings):
        for string in strings:
            self.lines.append((self.indentation * self.indentation_level) + string)

    def _dump(self, *args, **kwargs):
        return yaml.dump(*args, allow_unicode=True, **kwargs)[:-1]

    def _dump_string(self, string):
        if not isinstance(string, str):
            raise TypeError('Should have a string')
        return self._dump(string)[:-4]

    def _dump_keybinding(self, keybinding):
        
        self.add_lines('- keys: {}'.format(self._dump(keybinding['keys'])))
        self.indentation_level += 1
        self.add_lines('command: {}'.format(self._dump_string(keybinding['command'])))

        if 'command_mode_too' in keybinding and keybinding['command_mode_too'] is True:
            self.add_lines('command_mode_too: true')

        if 'args' in keybinding and keybinding['args'] != {}:
            self.add_lines('args:')
            self.indentation_level += 1
            self.add_lines(*self._dump(keybinding['args'], default_flow_style=False).split('\n'))
            self.indentation_level -= 1

        if 'context' in keybinding and keybinding['context'] != []:
            self.add_lines('context:')
            self.indentation_level += 1
            self.add_lines(*self._dump(keybinding['context'], default_flow_style=False).split('\n'))
            self.indentation_level -= 1
        self.indentation_level -= 1 


    def dump(self):
        for keybinding in self.keymap:
            self._dump_keybinding(keybinding)
            self.add_lines('')
        return '\n'.join(self.lines)

def yaml_dump(keymap):
    return YamlDumper(keymap).dump()
