# -*- encoding: utf-8 -*-

import yaml
from .constants import *
from .keymap_dumper import keymap_dump
from json import dumps
from re import compile as re_comp, escape as re_escape

SPLIT_KEYS = re_comp(r'(?<!\+), ?')

def pprint(*objs):
    for obj in objs:
        # CSW: ignore
        print(dumps(obj, indent=2, ensure_ascii=False))

def get_context_definitions(keybindings, errors):
    real_keybindings = []
    context_definitions = {}
    for keybinding in keybindings:
        if 'context_definitions' in keybinding.keys():
            context_definitions.update(keybinding['context_definitions'])
        else:
            real_keybindings.append(keybinding)
    return real_keybindings, context_definitions

def flatten_keybindings(keybindings, errors):
    valid_keybindings = []
    for keybinding in keybindings:
        if 'with_contexts' not in keybinding.keys():
            valid_keybindings.append(keybinding)
            continue

        if len(keybinding) != 1:
            extra_keys = list(keybinding)
            extra_keys.remove('with_contexts')
            errors.append("with_contexts object shouldn't "
                          "have any other keys. Got {}".format(', '.join(extra_keys)))

        context_names = set()
        for context_names_obj in keybinding['with_contexts']:
            if 'context_names' not in context_names_obj:
                continue
            else:
                context_names.update(context_names_obj['context_names'])

        for actual_keybinding in keybinding['with_contexts']:
            if 'context_names' in actual_keybinding:
                continue
            actual_keybinding.setdefault('include_contexts', []).extend(context_names)
            valid_keybindings.append(actual_keybinding)

    return valid_keybindings

def is_valid(keybinding):
    return 'keys' in keybinding and 'command' in keybinding

def include_contexts_to(keybinding, context_definitions):
    errors = []
    for name in keybinding['include_contexts']:
        try:
            context_definitions[name]
        except KeyError:
            errors.append('Including context', keybinding, 'not found', name)
        else:
            keybinding.setdefault('context', []).extend(context_definitions[name])
    return errors

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


    return (key.strip(),
            CONTEXT_OPERATORS[operator] if operator is not None else 'equal',
            # if there is no operator, there is no operand (so we take the default value)
            operand.strip() if operator is not None else True,
            match_all)

def format_context(keybinding):
    errors = []
    for i, context in enumerate(keybinding['context']):
        if isinstance(context, dict):
            continue
        key, operator, operand, match_all = split_context(context)
        keybinding['context'][i] = {
            'key': key,
        }

        if operand != True:
            keybinding['context'][i]['operand'] = operand

        if operator != 'equal':
            keybinding['context'][i]['operator'] = operator
            
        if match_all:
            keybinding['context'][i]['match_all'] = match_all


    return errors

def format_keys(keybinding, errors):
    keybinding['keys'] = list(map(str, keybinding['keys']))

def modify(keybindings, context_definitions, errors):
    for i, keybinding in enumerate(keybindings):

        if not is_valid(keybinding):
            errors += ['Not valid', keybinding]

        if 'include_contexts' in keybinding.keys():
            errors += include_contexts_to(keybinding, context_definitions)
            del keybinding['include_contexts']

        if 'context' in keybinding.keys():
            errors += format_context(keybinding)

        format_keys(keybinding, errors)

        if not keybinding.get('command_mode_too', False):
            keybinding.setdefault('context', []).append({'key': 'setting.command_mode', 'operand': False})
        keybinding.pop('command_mode_too', None)

    return keybindings

def print_formated_errors(errors):
    log('The following errors occurred:')
    for error in errors:
        log(error)

def to_keymap(yamlstring, dumper):
    errors = []
    keybindings = yaml.load(yamlstring)
    keybindings, context_definitions = get_context_definitions(keybindings, errors)
    keybindings = flatten_keybindings(keybindings, errors)
    keybindings = modify(keybindings, context_definitions, errors)
    if errors:
        print_formated_errors(errors)
        raise ValueError('Error(s) occurred, see output above.', errors)

    if dumper == 'minified':
        return dumps(keybindings, ensure_ascii=False)
    elif dumper == 'normal':
        return dumps(keybindings, indent='  ', ensure_ascii=False, sort_keys=True)
    elif dumper == 'custom':
        return keymap_dump(keybindings, indent='  ')
    else:
        raise ValueError('[Internal Error] Unknow dumper {!r}.'.format(dumper))
        

def main():
    with open(__file__ + '/../sample.sublime-yaml-keymap', encoding="utf-8") as fp:
        to_keymap(fp.read())

if __name__ == '__main__':
    main()