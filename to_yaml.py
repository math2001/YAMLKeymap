# -*- encoding: utf-8 -*-

from .constants import *
from .yaml_dumper import yaml_dump
import json

def format_context(keybinding):
    for i, context in enumerate(keybinding['context']):
        keybinding['context'][i] = "{} {}{} {}".format(context['key'],
                                                       CONTEXT_OPERATORS_INVERSE[context.get('operator', 'equal')],
                                                       '@' if context.get('match_all', False) else '',
                                                       context.get('operand', "true"))

def format_keys(keybinding):
    for i, key in enumerate(keybinding['keys']):
        if key.isdigit():
            keybinding['keys'][i] = int(key)


def add_command_mode_key(keybinding):
    if 'context' not in keybinding or 'setting.command_mode == False' not in keybinding['context']:
        keybinding['command_mode_too'] = True

    if 'context' in keybinding and 'setting.command_mode == False' in keybinding['context']:
        keybinding['context'].remove('setting.command_mode == False')

def modify(keymap):
    for keybinding in keymap:
        format_keys(keybinding)

        if 'context' in keybinding:
            format_context(keybinding)

        add_command_mode_key(keybinding)

        if keybinding.get('context', None) == []:
            del keybinding['context']

    return keymap

def to_yaml(keymap):
    return yaml_dump(modify(json.loads(keymap)))
