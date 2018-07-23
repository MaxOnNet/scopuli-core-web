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

from jinja2 import nodes
from werkzeug.local import LocalProxy


class WebWidget:
    def __init__(self, environment, widget_config, widget_uuid):
        self._environment = environment
        self._widget_config = widget_config
        self._widget_uuid = widget_uuid
        self._application = self._environment.app
        self._config = self._application.config_xml
        self._database = LocalProxy(self._application.database.request_get)
        
        self._site = self._application.site
    
        self.load()
        
    def load(self):
        pass


    @property
    def application(self):
        """
            Свойство возвращающее текущее приложение.

            :return: Загруженный обьект :ref:`module-web-application`
            :rtype: :ref:`module-web-application`
        """
        return self._application


    @property
    def config(self):
        """
            Свойство возвращающее текущий конфиг.

            :return: Загруженный обьект :ref:`module-interfaces-config`
            :rtype: :ref:`module-interfaces-config`
        """
        return self._config
    
    @property
    def uuid(self):
        return self._widget_uuid
    
    
    def render(self):
        property_names = [p for p in dir(WebWidget) if isinstance(getattr(WebWidget, p), property)]
        
        for prop in property_names:
            self._config.items.append(nodes.Pair(nodes.Const(prop), nodes.Const(getattr(self, prop))))
        
        # dict = Dict(items)
        # dict.set_lineno(self.config.lineno)
        # dict.set_environment(self.config.environment)
        
        return self._config
