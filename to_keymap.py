# -*- encoding: utf-8 -*-

import yaml
from json import dumps
from re import compile as re_comp

SPLIT_KEYS = re_comp(r'(?<!\+), ?')

def pprint(*objs):
    for obj in objs:
        # CSW: ignore
        print(dumps(obj, indent=2, ensure_ascii=False))

def get_context_definitions(keybindings):
    real_keybindings = []
    context_definitions = {}
    for keybinding in keybindings:
        if 'context_definitions' in keybinding.keys():
            context_definitions.update(keybinding['context_definitions'])
        else:
            real_keybindings.append(keybinding)
    return real_keybindings, context_definitions


def include_contexts_to(keybinding, context_definitions):
    errors = []
    for name in keybinding['include_contexts']:
        try:
            context_definitions[name]
        except KeyError:
            errors.append(['Including context', keybinding, 'not found', name])
        else:
            keybinding.setdefault('context', []).append(context_definitions[name])
    return errors

def format_key(keybinding):
    if isinstance(keybinding, list):
        return []

    if '+' in keybinding['keys']:
        keybinding['keys'] = SPLIT_KEYS.split(keybinding['keys'])
    else:
        keybinding['keys'] = list(keybinding['keys'])
    return []

def is_valid(keybinding):
    return 'keys' in keybinding and 'command' in keybinding

def modify(keybindings, context_definitions):
    errors = []
    for i, keybinding in enumerate(keybindings):

        if not is_valid(keybinding):
            errors += ['Not valid', keybinding]

        if 'include_contexts' in keybinding.keys():
            errors += include_contexts_to(keybinding, context_definitions)
            del keybinding['include_contexts']

        errors += format_key(keybinding)

    return keybindings, errors

def to_keymap(yamlstring):
    keybindings = yaml.load(yamlstring)
    keybindings, context_definitions = get_context_definitions(keybindings)
    keybindings, errors = modify(keybindings, context_definitions)
    pprint(keybindings, errors)

with open('sample.sublime-yaml-keymap', encoding="utf-8") as fp:
    to_keymap(fp.read())