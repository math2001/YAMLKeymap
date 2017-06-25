# -*- encoding: utf-8 -*-

import os
import yaml

def to_keymap(yamlstring):
    keymaps = yaml.load(yamlstring)
    # add_insert_mode_context

def files_to_keymap(yaml_files):
    for file in yaml_files:
        with open(os.path.splitext(file)[0] + '.sublime-keymap'):
            fp.write(to_keymap(file, isfile=True))

