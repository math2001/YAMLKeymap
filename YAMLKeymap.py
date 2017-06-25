# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os.path

from .constants import *
from .api import *

class YamlKeymapCommand(sublime_plugin.EventListener):
    
    def on_post_save(self, view):
        if os.path.splitext(view.file_name())[1] == YAML_EXTENSION:
            file_to_keymap(view.file_name())