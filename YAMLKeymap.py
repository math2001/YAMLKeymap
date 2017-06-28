# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os.path

from .constants import *
from .api import *

class RunYamlKeymapActionCommand(sublime_plugin.ApplicationCommand):

    def to_keymap_action(self, files):
        for file in files:
            sublime.expand_variables(self.window.exctract_variable())
            try:
                file_to_keymap(file)
            except Exception as e:
                # CSW: ignore
                print("YAMLKeymap error: cannot convert {!r}", e)

    def migrate_action(self, force=False):
        to_migrate = []
        for root, dirs, files in os.walk(sublime.packages_path()):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                if os.path.splitext(file)[1] == JSON_EXTENSION:
                    to_migrate.append(file)

        for file in to_migrate:
            if os.path.exists(get_dst_file_name(file)) and force is not True:
                # CSW: ignore
                print("YAMLKeymap: cannot migrate {}, destination already exists. Delete it, or "
                      "set force to True in the arguments")
            else:
                to_yaml(file)

    def run(self, edit, action, *args, **kwargs):
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