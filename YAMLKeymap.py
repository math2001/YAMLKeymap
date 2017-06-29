# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os

from .constants import *
from .api import *

class RunYamlKeymapActionCommand(sublime_plugin.ApplicationCommand):

    def to_keymap_action(self, files):
        for file in files:
            file = sublime.expand_variables(file, self.window.extract_variables())
            try:
                file_to_keymap(file)
            except Exception as e:
                # CSW: ignore
                print("YAMLKeymap error: cannot convert {!r}".format(file), e)

    def migrate_action(self, frompath="", force=False):
        to_migrate = []
        for root, dirs, files in os.walk(os.path.join(sublime.packages_path(), frompath)):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                if os.path.splitext(file)[1] == JSON_EXTENSION:
                    to_migrate.append(os.path.join(root, file))

        for file in to_migrate:
            if os.path.exists(get_dst_file_name(file)) and force is not True:
                # CSW: ignore
                print("YAMLKeymap: cannot migrate {}, destination already exists. Delete it, or "
                      "set force to True in the arguments")
            else:
                file_to_yaml(file)

    def run(self, action, *args, **kwargs):
        self.window = sublime.active_window()
        try:
            function = getattr(self, action + '_action')
        except AttributeError:
            return sublime.error_message("YAMLKeymap: "
                                         "Couldn't find the action '{}'".format(action))
        function(*args, **kwargs)


class YamlKeymapCommand(sublime_plugin.EventListener):
    
    def on_post_save(self, view):
        if os.path.splitext(view.file_name())[1] == YAML_EXTENSION:
            sublime.run_command('run_yaml_keymap_action', {'action': 'to_keymap', 'files': ['$file']})