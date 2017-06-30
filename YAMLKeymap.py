# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os

from .constants import *
from .api import *


class RunYamlKeymapActionCommand(sublime_plugin.ApplicationCommand):

    def to_keymap_action(self, files):

        if get_settings().get('minify_output') is True:
            dumper = 'minified'
        elif get_settings().get('use_custom_json_dumper') is True:
            dumper = 'custom'
        else:
            dumper = 'normal'

        for file in files:
            file = sublime.expand_variables(file, self.window.extract_variables())
            try:
                file_to_keymap(file, dumper=dumper)
            except Exception as e:
                if is_dev():
                    raise e
                log(error_to_string("YAMLKeymap error: cannot convert {!r}".format(file), e))

    def migrate_action(self, frompath="", force=False):
        to_migrate = []
        frompath = os.path.join(sublime.packages_path(), frompath)
        if os.path.isfile(frompath):
            to_migrate = [frompath]
        else:
            for root, dirs, files in os.walk(frompath):
                if '.git' in dirs:
                    dirs.remove('.git')
                for file in files:
                    if os.path.splitext(file)[1] == JSON_EXTENSION:
                        to_migrate.append(os.path.join(root, file))

        errors = 0
        fails = 0
        for file in to_migrate:
            if os.path.exists(get_dst_file_name(file)) and force is not True:
                log("Cannot migrate {}, destination already exists. Delete it, or "
                      "set the argument 'force' to True".format(file))
                errors += 1
            else:
                error = file_to_yaml(file)
                if error is not None:
                    log(error)
                    fails += 1

        log('Migrated {} file(s) ({} fail(s) on {} file(s))'.format(len(to_migrate) - errors, fails,
                                                                  len(to_migrate)))


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
        if get_settings().get('convert_on_save') is not True:
            return

        if os.path.splitext(view.file_name())[1] == YAML_EXTENSION:
            sublime.run_command('run_yaml_keymap_action', {'action': 'to_keymap', 'files': ['$file']})