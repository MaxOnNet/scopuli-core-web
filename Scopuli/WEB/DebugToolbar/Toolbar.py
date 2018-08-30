#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2017] Tatarnikov Viktor [viktor@tatarnikov.org]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from flask import url_for, current_app
from werkzeug.utils import import_string


class DebugToolbar(object):

    _cached_panel_classes = {}

    def __init__(self, request, jinja_env):
        self.jinja_env = jinja_env
        self.request = request
        self.panels = []

        self.template_context = {
            'static_path': '/static/debug_panel/'
        }

        self.create_panels()

    def create_panels(self):
        """
        Populate debug panels
        """
        activated = self.request.cookies.get('fldt_active', '')
        activated = unquote(activated).split(';')

        for panel_class in self._iter_panels(current_app):
            panel_instance = panel_class(jinja_env=self.jinja_env,
                                         context=self.template_context)

            if panel_instance.dom_id() in activated:
                panel_instance.is_active = True

            self.panels.append(panel_instance)

    def render_toolbar(self):
        context = self.template_context.copy()
        context.update({'panels': self.panels})

        template = self.jinja_env.get_template('base.html')
        return template.render(**context)

    @classmethod
    def load_panels(cls, app):
        for panel_class in cls._iter_panels(app):
            # just loop to make sure they've been loaded
            pass

    @classmethod
    def _iter_panels(cls, app):
        for panel_path in app._config.get("web", "debug-toolbar", "panels", "").split(";"):
            panel_class = cls._import_panel(app, "WEB.DebugToolbar.Panels.{}".format(panel_path))
            if panel_class is not None:
                yield panel_class

    @classmethod
    def _import_panel(cls, app, path):
        cache = cls._cached_panel_classes

        try:
            return cache[path]
        except KeyError:
            pass

        try:
            panel_class = import_string(path)
        except ImportError as e:
            app.logger.warning('Disabled %s due to ImportError: %s', path, e)
            panel_class = None

        cache[path] = panel_class
        return panel_class
