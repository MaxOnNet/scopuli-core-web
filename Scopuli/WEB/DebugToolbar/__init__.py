#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2018] Tatarnikov Viktor [viktor@tatarnikov.org]
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
""" """

import os
import warnings
import logging

from flask import Blueprint, current_app, request, g, send_from_directory
from flask.globals import _request_ctx_stack
from jinja2 import Environment, FileSystemLoader
from werkzeug.urls import url_quote_plus as filter_url_encode

from Scopuli.WEB.DebugToolbar.Compat import iteritems
from Scopuli.WEB.DebugToolbar.Toolbar import DebugToolbar
 

from Scopuli.Interfaces.WEB.Jinja.Filters import filter_printable

module = Blueprint('debugtoolbar', __name__)
log = logging.getLogger(__name__)


def replace_insensitive(string, target, replacement):
    """Similar to string.replace() but is case insensitive
    Code borrowed from:
    http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else:  # no results so return the original string
        return string


class DebugToolbarExtension(object):
    _redirect_codes = [301, 302, 303, 304]

    def __init__(self, app=None):
        self._application = app
        self.debug_toolbars = {}
        
        self.__static_folder = "{0}/debug_panel".format(self._application._config.get("web", "application", "static_folder", "/static"))
        self.__static_folder_master = "{0}/debug_panel".format(self._application._config.get("web", "application", "static_folder_master", "/static"))
        self.__template_folder = "{0}/debug_panel".format(self._application._config.get("web", "application", "template_folder", "/templates"))
        self.__template_folder_master = "{0}/debug_panel".format(self._application._config.get("web", "application", "template_folder_master", "/templates"))

        self.jinja_env = Environment(
            autoescape=True,
            extensions=['jinja2.ext.i18n', 'jinja2.ext.with_'],
            loader=FileSystemLoader([self.__template_folder, self.__template_folder_master]))
        
        # подключаем фильтры для шаблонизатора
        self.jinja_env.filters['urlencode'] = filter_url_encode
        self.jinja_env.filters['printable'] = filter_printable

        if self._application is not None:
            if self._application._config.get("web", "debug-toolbar", "enable", "False") == "False":
                return None
    
            if not self._application.secret_key:
                log.error("The DebugToolbar requires the 'SECRET_KEY' config var to be set.")
                return None
            
            DebugToolbar.load_panels(self._application)
    
            self._application.before_request(self.process_request)
            self._application.after_request(self.process_response)
            self._application.teardown_request(self.teardown_request)
    
            # Monkey-patch the Flask.dispatch_request method
            self._application.dispatch_request = self.dispatch_request
    
            self._application.add_url_rule('/debug_toolbar/static/<path:filename>',
                             'debug_toolbar.static', self.send_static_file)
    
            self._application.register_blueprint(module, url_prefix='/debug_toolbar/views')

    def dispatch_request(self):
        """Modified version of Flask.dispatch_request to call process_view."""
        req = _request_ctx_stack.top.request
        app = current_app

        if req.routing_exception is not None:
            app.raise_routing_exception(req)

        rule = req.url_rule

        # if we provide automatic options for this URL and the
        # request came with the OPTIONS method, reply automatically
        if getattr(rule, 'provide_automatic_options', False) \
           and req.method == 'OPTIONS':
            return app.make_default_options_response()

        # otherwise dispatch to the handler for that endpoint
        view_func = app.view_functions[rule.endpoint]
        view_func = self.process_view(app, view_func, req.view_args)

        return view_func(**req.view_args)

    def _show_toolbar(self):
        """Return a boolean to indicate if we need to show the toolbar."""
        if request.blueprint == 'debugtoolbar':
            return False

        hosts = self._application._config.get("web", "debug-toolbar", "hosts", "127.0.0.1").split(";")
        # Nginx Proxy support
        if 'X-Real-IP' in request.headers:
            if request.headers['X-Real-IP'] in hosts:
                return True
        else:
            if request.remote_addr in hosts:
                return True

        return False

    def send_static_file(self, filename):
        if os.path.exists("{}/{}".format(self.__static_folder, filename)):
            return send_from_directory(self.__static_folder, filename)

        if os.path.exists("{}/{}".format(self.__static_folder_master, filename)):
            return send_from_directory(self.__static_folder_master, filename)

    def process_request(self):
        g.debug_toolbar = self

        if not self._show_toolbar():
            return

        real_request = request._get_current_object()

        self.debug_toolbars[real_request] = (
            DebugToolbar(real_request, self.jinja_env))

        for panel in self.debug_toolbars[real_request].panels:
            panel.process_request(real_request)

    def process_view(self, app, view_func, view_kwargs):
        """ This method is called just before the flask view is called.
        This is done by the dispatch_request method.
        """
        real_request = request._get_current_object()
        try:
            toolbar = self.debug_toolbars[real_request]
        except KeyError:
            return view_func

        for panel in toolbar.panels:
            new_view = panel.process_view(real_request, view_func, view_kwargs)
            if new_view:
                view_func = new_view

        return view_func

    def process_response(self, response):
        real_request = request._get_current_object()
        if real_request not in self.debug_toolbars:
            return response

        # Intercept http redirect codes and display an html page with a
        # link to the target.
        if self._application._config.get("web", "debug-toolbar", "intercept_redirects", "True") == "True":
            if (response.status_code in self._redirect_codes and
                    not real_request.is_xhr):
                redirect_to = response.location
                redirect_code = response.status_code
                if redirect_to:
                    content = self.render('redirect.html', {
                        'redirect_to': redirect_to,
                        'redirect_code': redirect_code
                    })
                    response.content_length = len(content)
                    response.location = None
                    response.response = [content]
                    response.status_code = 200

        # If the http response code is 200 then we process to add the
        # toolbar to the returned html response.
        if not (response.status_code == 200 and
                response.is_sequence and
                response.headers['content-type'].startswith('text/html')):
            return response

        response_html = response.data.decode(response.charset)

        no_case = response_html.lower()
        body_end = no_case.rfind('</body>')

        if body_end >= 0:
            before = response_html[:body_end]
            after = response_html[body_end:]
        elif no_case.startswith('<!doctype html>'):
            before = response_html
            after = ''
        else:
            log.warning('Нет возможности использовать Debug Toolbar, ответ сервера не является валидным HTML')
            return response

        toolbar = self.debug_toolbars[real_request]

        for panel in toolbar.panels:
            panel.process_response(real_request, response)

        toolbar_html = toolbar.render_toolbar()

        content = ''.join((before, toolbar_html, after))
        content = content.encode(response.charset)
        response.response = [content]
        response.content_length = len(content)

        return response

    def teardown_request(self, exc):
        self.debug_toolbars.pop(request._get_current_object(), None)

    def render(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
