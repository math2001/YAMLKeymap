# -*- encoding: utf-8 -*-

import yaml
from .constants import *
from .keymap_encoder import keymap_encode
from json import dumps
from re import compile as re_comp, escape as re_escape

SPLIT_KEYS = re_comp(r'(?<!\+), ?')

CONTEXT_OPERATORS = {
    
    '==': 'equal',
    '!=': 'not_equal',
    '^==': 'regex_match',
    '^!=': 'not_regex_match',
    '*==': 'regex_contains',
    '*!=': 'not_regex_contains',

}

def split_context(string):

    key = ''
    operator = None
    operand = ''
    match_all = False

    continue_till = 0

    def get_operator_following(string, i):
        for operator in CONTEXT_OPERATORS.keys():
            if string[i:].find(operator) == 0:
                return operator

    for i, char in enumerate(string):
        if i < continue_till:
            continue
        found_operator = get_operator_following(string, i)
        if operator is None:
            if found_operator is not None:
                operator = found_operator
                continue_till = i + len(operator)
            else:
                key += char

        elif operand == '' and char == '@':
            match_all = True

        else:
            operand += char


    return key.strip(), CONTEXT_OPERATORS[operator], operand.strip(), match_all

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
            keybinding.setdefault('context', []).extend(context_definitions[name])
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

def format_context(keybinding):
    errors = []
    for i, context in enumerate(keybinding['context']):
        if isinstance(context, dict):
            continue
        key, operator, operand, match_all = split_context(context)
        keybinding['context'][i] = {
            'key': key,
            'operand': operand,
        }
        if operator != 'equal':
            keybinding['context'][i]['operator'] = operator
            
        if match_all:
            keybinding['context'][i]['match_all'] = match_all


    return errors

def modify(keybindings, context_definitions):
    errors = []
    for i, keybinding in enumerate(keybindings):

        if not is_valid(keybinding):
            errors += ['Not valid', keybinding]

        if 'include_contexts' in keybinding.keys():
            errors += include_contexts_to(keybinding, context_definitions)
            del keybinding['include_contexts']

        errors += format_key(keybinding)

        if 'context' in keybinding.keys():
            errors += format_context(keybinding)

        if not keybinding.get('vimMode', False):
            keybinding.setdefault('context', []).append({'key': 'setting.command_mode', 'operand': False})
        keybinding.pop('vimMode', None)

    return keybindings, errors

def to_keymap(yamlstring):
    keybindings = yaml.load(yamlstring)
    keybindings, context_definitions = get_context_definitions(keybindings)
    keybindings, errors = modify(keybindings, context_definitions)
    if errors:
        print_formated_errors(errors)
        exception = ConversionError('Error(s) occurred, see output above.')
        exception.errors = errors
        raise exception
    return keymap_encode(keybindings)

def main():
    with open(__file__ + '/../sample.sublime-yaml-keymap', encoding="utf-8") as fp:
        to_keymap(fp.read())

if __name__ == '__main__':
    main()