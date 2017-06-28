# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import os.path

class YAMLKeymapDevListener(sublime_plugin.EventListener):

    def on_post_save(self, view):
        if not (os.path.dirname(__file__) in view.file_name() and
            view.file_name().endswith('.py')):
            return
        sublime.run_command('reload_plugin', {
            'main': os.path.join(sublime.packages_path(), 'YAMLKeymap',
                                 'YAMLKeymap.py'),
            'scripts': ['constants', 'api', 'to_keymap'],
            'folders': ['tests'],
            'quiet': True
        })
