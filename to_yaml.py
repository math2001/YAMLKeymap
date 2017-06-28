# -*- encoding: utf-8 -*-

from .constants import *
import json
import yaml

from collections import OrderedDict

def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

def format_context(keybinding):
    for i, context in enumerate(keybinding['context']):
        keybinding['context'][i] = "{} {}{} {}".format(context['key'],
                                                       CONTEXT_OPERATORS_INVERSE[context.get('operator', 'equal')],
                                                       '@' if context.get('match_all', False) else '',
                                                       context.get('operand', True))

def format_keys(keybinding):
    for key in keybinding['keys']:
        if len(key) != 1:
            return

    keybinding['keys'] = ''.join(keybinding['keys'])

def add_command_mode_key(keybinding):
    if 'context' not in keybinding or 'setting.command_mode == False' not in keybinding['context']:
        keybinding['command_mode_too'] = True

def modify(keymap):
    for keybinding in keymap:
        format_keys(keybinding)

        if 'context' in keybinding:
            format_context(keybinding)

        add_command_mode_key(keybinding)

    return keymap

yaml.add_representer(OrderedDict, represent_ordereddict)


def to_yaml(keymap):
    return yaml.dump(modify(json.loads(keymap, object_pairs_hook=OrderedDict)), 
                     default_flow_style=False, allow_unicode=True)

