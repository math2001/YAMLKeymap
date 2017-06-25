# -*- encoding: utf-8 -*-

import os
import yaml

from .to_keymap import to_keymap
from constants import *

def file_to_keymap(src):
    dst = os.path.splitext(src)[0] + JSON_EXTENSION
    with open(src, encoding='utf-8') as fp_src:
        with open(dst, 'w') as fp_dst:
            fp_dst.write(to_keymap(fp_src.read()))


def files_to_keymap(yaml_files):
    for file in yaml_files:
        try:
            file_to_keymap(file)
        except ConversionError:
            # CSW: ignore
            print(ConversionError)
