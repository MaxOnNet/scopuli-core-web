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

import sys
import os
import logging
import logging.handlers
import threading
import htmlmin
import bs4

# from Scopuli.WEB.DebugToolbar import DebugToolbarExtension as ExtensionDebugToolbar

import Scopuli.Interfaces.WEB.Jinja.Tools as JinjaTool
import Scopuli.Interfaces.WEB.Jinja.Extensions as JinjaExt
import Scopuli.Interfaces.WEB.Jinja.Filters as JinjaFil

import Scopuli.WEB.Application as WebApplication
import ApplicationModules as WebModules
import ApplicationWidgets as WebWidgets


log = logging.getLogger(__name__)


class Application(WebApplication.Application):
    def _register_extensions(self):
        """
            Загружаем дополнения для Jinja2 окружения, такие как парсеры ополнительных тэгов.

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Extensions.")
        
        self.jinja_env.add_extension(JinjaExt.MetaInfoExtension)
        self.jinja_env.add_extension(JinjaExt.WidgetExtension)
        self.jinja_env.add_extension(JinjaExt.TimeExtension)
    
    
    def _register_filters(self):
        """
            Загружаем фильтров для Jinja2 окружения, такие как рендер MarkDown'a.

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Filters.")
        
        self.jinja_env.filters['markdown'] = JinjaFil.filter_markdown
        self.jinja_env.filters['shuffle'] = JinjaFil.filter_shuffle
        self.jinja_env.filters['phonenumber'] = JinjaFil.filter_phonenumber
        self.jinja_env.filters['money'] = JinjaFil.filter_money
    
    
    def _register_hooks(self):
        """
            Загружаем так называемые хуки или костыли.

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Hooks.")
        
        WebModules.HookFavicon(self).register()
    
    
    def _register_modules(self):
        """
            Загружаем основные модули приложения, к примеру поддержку сессий, аналитика, поддержка robots.txt и sitemap.xml

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Modules.")
        
        # Core
        WebModules.Session(self).register()
        WebModules.Permissions(self).register()
        
        # Search Robots
        WebModules.Robots(self).register()
        WebModules.Sitemap(self).register()
        
        # SEO
        WebModules.Analytics(self).register()
    
    
    def _register_errors(self):
        """
            Загружаем страницы ошибок 400, 401, 404.

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Errors.")
        
        WebModules.Error_400(self).register()  # Ошибка в данных запроса
        WebModules.Error_401(self).register()  # Ошибка доступа
        WebModules.Error_404(self).register()  # Страница не найдена
    
    
    def _register_pages(self):
        """
            Загружаем страницы приложения, которые описаны в базе данных.

            :return: None
            :rtype: Nothing
        """
        log.info("App: Register Pages.")
        
        for page in self._site.pages:
            if page.is_enable:
                page.module.register()


if __name__ == '__main__':
    # Подсветка выхлопа, только для дебага, что бы не засорять логи спец символами
    import Scopuli.Console.Logging.Colorer
    
    
    webapp = Application()
    webapp.run(threaded=True, host="0.0.0.0", port=5000)
