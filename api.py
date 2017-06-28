# -*- encoding: utf-8 -*-

import os
import yaml

from .to_keymap import to_keymap
from .to_yaml import to_yaml
from .constants import *

def get_dst_file_name(src):
    path, ext = os.path.splitext(src)
    if ext == JSON_EXTENSION:
        return path + YAML_EXTENSION
    else:
        return path + JSON_EXTENSION

def file_to_keymap(src):
    with open(src, encoding='utf-8') as fp_src:
        keymap = to_keymap(fp_src.read())

    with open(get_dst_file_name(src), 'w', encoding='utf-8') as fp_dst:
        fp_dst.write(keymap)

def file_to_yaml(src):
    with open(src, encoding='utf-8') as fp_src:
        yaml = to_yaml(fp_src.read())

    with open(get_dst_file_name(src), 'w', encoding='utf-8') as fp_dst:
        fp_dst.write(yaml)
