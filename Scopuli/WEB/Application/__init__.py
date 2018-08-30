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

import sys
import os
import logging
import logging.handlers
import threading
import htmlmin
import bs4

from flask import Flask, jsonify, render_template, request, abort
from flask.helpers import send_from_directory, locked_cached_property

from werkzeug.local import LocalProxy

from jinja2 import FileSystemLoader

# from Scopuli.WEB.DebugToolbar import DebugToolbarExtension as ExtensionDebugToolbar

from Scopuli.Interfaces.Config import Config
from Scopuli.Interfaces.WEB import WebSite, WebDatabase

import Scopuli.Interfaces.WEB.Jinja.Tools as JinjaTool
import Scopuli.Interfaces.WEB.Jinja.Extensions as JinjaExt
import Scopuli.Interfaces.WEB.Jinja.Filters as JinjaFil

import Scopuli.WEB.Modules as WebModules


log = logging.getLogger(__name__)


class Application(Flask):
    """
        При инициализации, загружается конфигурационный фаил на основе данных которого инициализируется Flask.

        Для инициализации требуются следующий параметры в конфигурационном файле:

        #. **site_id** - Идентификатор сайта в базе данных, подробнее в описании таблицы :ref:`module-interfaces-mysql-schema-web`.
        #. **import_name** - Имя импортирования во Flask (оставлять не изменным)
        #. **static_url_path** - Относительный путь до папки со статическими файлами
        #. **static_folder** - Полный путь до папки со статическими файлами сайта
        #. **static_folder_master** - Полный путь до папки со статическими файлами проекта, если будет запрощен статический фаил, и он не будет найден в папке сайта, то будет произведен поиск файла из данной папки
        #. **template_folder** - Полный путь до папки с Jinja2 шаблонами сайта
        #. **template_folder_master** - Полный путь до папки с Jinja2 шаблонами проекта, если будет запрощен шаблон, и он не будет найден в папке сайта, то будет произведен поиск файла из данной папки

        Пример "второго" (подробнее :ref:`module-interfaces-config` и :ref:`example-config-4gw`) конфигурационного файла:

        .. code-block:: xml
            :linenos:

            <?xml version="1.0" encoding="UTF-8"?>
            <configuration>
                <web site_id="1">
                    <application import_name="forGain"
                                 static_url_path="/static"
                                 static_folder="/home/apache/pro-4gain-www/.4gain.web/static"
                                 static_folder_master="/home/apache/pro-4gain-www/.4gain/share/static"
                                 template_folder="/home/apache/pro-4gain-www/.4gain.web/templates/default"
                                 template_folder_master="/home/apache/pro-4gain-www/.4gain/share/templates/default"/>
                </web>
            </configuration>

    """
    _config_file = "./config.xml"
    
    def __init__(self):
        """

        """
        self._config = Config(path=self._config_file)
        
        self._logging_init()
        
        self.__register_modules = {}
        
        self.__import_name = self._config.get("web", "application", "import_name", "forGain")
        self.__static_url_path = self._config.get("web", "application", "static_url_path", "/static")
        self.__static_folder = self._config.get("web", "application", "static_folder", "/static")
        self.__static_folder_master = self._config.get("web", "application", "static_folder_master", "/static")
        self.__template_folder = self._config.get("web", "application", "template_folder", "/templates")
        self.__template_folder_master = self._config.get("web", "application", "template_folder_master", "/templates")
        
        super(Application, self).__init__(import_name=self.__import_name, static_url_path=self.__static_url_path,
                                          static_folder=self.__static_folder, template_folder=self.__template_folder)
        
        # Config settings for debug
        self.config['DEBUG'] = True
        self.config['TEMPLATES_AUTO_RELOAD'] = True
        
        # Вынести настройку данных массивов в module_register
        self.__render_callback_modules = ['Session', 'Permissions', 'Account', 'Analytics']
        self.__render_callback_modules_json = ['Permissions', 'Account']
        
        self._database = WebDatabase(self)
        self._site = WebSite(self)
        
        self._register_extensions()
        self._register_filters()
        self._register_hooks()
        self._register_errors()
        self._register_modules()
        self._register_pages()
        
        # Активируем глобальные дополнения отладки
        # ExtensionDebugToolbar(self)
        
        # Закрываем транзакцию.
        self._database_unload()
    
    
    @property
    def site(self):
        """
            Свойство возвращающее текущий сайт.

            :return: Загруженный обьект :ref:`module-interfaces-web-site`
            :rtype: :ref:`module-interfaces-web-site`
        """
        return self._site
    
    
    @property
    def config_xml(self):
        """
            Свойство возвращающее текущий конфиг.

            :return: Загруженный обьект :ref:`module-interfaces-config`
            :rtype: :ref:`module-interfaces-config`
        """
        return self._config
    
    
    @property
    def database(self):
        """
            Свойство возвращающее текущeую базу данных.

            :return: Загруженный обьект :ref:`module-interfaces-web-database`
            :rtype: :ref:`module-interfaces-web-database`
        """
        return self._database
    
    
    def _logging_init(self):
        """
            Функция инициализации подсистемы логирования

            :return: None
            :rtype: Nothing
        """
        threading.current_thread().name = 'main'
        
        logging.basicConfig(level=int(self._config.get("logging", "console", "level", "10")), stream=sys.stdout,
                            format='%(asctime)s [{}] [%(module)15s] [%(funcName)21s] [%(lineno)4d] [%(levelname)7s] [%(threadName)10s] %(message)s'.format(
                                int(self._config.get("web", "", "site_id", "-1"))))
        
        log_handler_console = logging.StreamHandler()
        log_handler_console.setLevel(int(self._config.get("logging", "console", "level", "10")))
        log_handler_console.setFormatter(
                logging.Formatter(
                    '%(asctime)s [{}] [%(module)15s] [%(funcName)21s] [%(lineno)4d] [%(levelname)7s] [%(threadName)10s] %(message)s'.format(
                        int(self._config.get("web", "", "site_id", "-1")))))
        
        if bool(int(self._config.get("logging", "", "use_file", "0"))):
            log_handler_file = logging.handlers.TimedRotatingFileHandler(self._config.get("logging", "file", "path", "4gain.log"),
                                                                         when=self._config.get("logging", "file", "when", "d"),
                                                                         interval=int(self._config.get("logging", "file", "interval", "1")),
                                                                         backupCount=int(self._config.get("logging", "file", "count", "1")))
            log_handler_file.setLevel(int(self._config.get("logging", "file", "level", "10")))
            log_handler_file.setFormatter(logging.Formatter(
                    '%(asctime)s [{}] [%(module)15s] [%(funcName)21s] [%(lineno)4d] [%(levelname)7s] [%(threadName)10s] %(message)s'.format(
                        int(self._config.get("web", "", "site_id", "-1")))))
            
            logging.getLogger('').addHandler(log_handler_file)
        
        if bool(int(self._config.get("logging", "", "use_syslog", "0"))):
            log_handler_syslog = logging.handlers.SysLogHandler(address=(self._config.get("logging", "syslog", "address_ip", "127.0.0.1"),
                                                                         int(self._config.get("logging", "syslog", "address_port", "514"))))
            log_handler_syslog.setLevel(int(self._config.get("logging", "file", "level", "10")))
            log_handler_syslog.setFormatter(logging.Formatter(
                    '%(asctime)s [{}] [%(module)15s] [%(funcName)21s] [%(lineno)4d] [%(levelname)7s] [%(threadName)10s] %(message)s'.format(
                        int(self._config.get("web", "", "site_id", "-1")))))
            
            logging.getLogger('').addHandler(log_handler_syslog)
        
        # logging.getLogger('').addHandler(log_handler_console)
        
        log.info("App: Logging Enable.")
    
    
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
    
    
    def _database_unload(self):
        """
            Функция закрытия первичного соеденения с БД, используемого для загрузки информации о сайте и подгружаемых модулях.

            :return: None
            :rtype: Nothing
        """
        self._database._context_teardown(None)
    
    
    def render(self, template, web_page, web_module, http_code=200):
        """
            Функция отрисовки страницы на основе шаблона, и переданных классов web_module и web_page.

            :param template: Путь до шаблона
            :type template: String
            :param web_page: Экземпляр класса :ref:`module-interfaces-web-page`
            :type web_page: :ref:`module-interfaces-web-page`
            :param web_module: Экземпляр класса  :ref:`module-interfaces-web-module`
            :type web_module: :ref:`module-interfaces-web-module`
            :param http_code: HTTP Return status code
            :type http_code: Integer
            :return: Отрисованное содержание страницы
            :rtype: String
        """
        self.render_callback(template, web_page, web_module)
        
        render_html = render_template(template, site=self._site, page=web_page, module=web_module, widgets={}, meta={},
                                      session=self.module_instance("Session"))
        
        # Дополнение, по минимализации выходного HTML кода
        if self._config.get("web", "addon-html-minifer", "enable", "True") == "True":
            render_html = htmlmin.minify(render_html, remove_comments=True, remove_empty_space=True)
        
        # дополнение, по переформатированию HTML кода для лучшего прочнения человеком
        if self._config.get("web", "addon-html-beautiful", "enable", "False") == "True":
            render_html_soup = bs4.BeautifulSoup(render_html, 'html.parser')
            render_html = render_html_soup.prettify()
        
        return render_html, http_code
    
    
    def render_json(self, json_object, web_page, web_module, http_code=200):
        """
            Функция серилизации и отправки JSON.

            :param json_object: JSON Dict
            :type json_object: Dict
            :param web_page: Экземпляр класса :ref:`module-interfaces-web-page`
            :type web_page: :ref:`module-interfaces-web-page`
            :param web_module: Экземпляр класса  :ref:`module-interfaces-web-module`
            :type web_module: :ref:`module-interfaces-web-module`
            :param http_code: HTTP Return status code
            :type http_code: Integer
            :return: Отрисованное содержание страницы
            :rtype: String
        """
        self.render_callback_json(web_page, web_module)
        
        return jsonify(json_object), http_code
    
    
    def render_callback(self, template, web_page, web_module):
        """
            Функция вызываемая перед каждой отрисовке шаблона, она перебирает список загруженных модулей помеченных для получения этого вызова.

            :param template: Путь до шаблона
            :type template: String
            :param web_page: Экземпляр класса :ref:`module-interfaces-web-page`
            :type web_page: :ref:`module-interfaces-web-page`
            :param web_module: Экземпляр класса  :ref:`module-interfaces-web-module`
            :type web_module: :ref:`module-interfaces-web-module`
            :return: None
        """
        for instance_name in self.__render_callback_modules:
            instance_module = self.module_instance(instance_name)
            
            if instance_module:
                instance_module.callback_render(template, web_page, web_module)
    
    
    def render_callback_json(self, web_page, web_module):
        """
            Функция вызываемая перед каждой отсылкой JSON, она перебирает список загруженных модулей помеченных для получения этого вызова.

            :param web_page: Экземпляр класса :ref:`module-interfaces-web-page`
            :type web_page: :ref:`module-interfaces-web-page`
            :param web_module: Экземпляр класса  :ref:`module-interfaces-web-module`
            :type web_module: :ref:`module-interfaces-web-module`
            :return: None
        """
        for instance_name in self.__render_callback_modules_json:
            instance_module = self.module_instance(instance_name)
            
            if instance_module:
                instance_module.callback_render(None, web_page, web_module)
    
    
    def module_register(self, name, instance):
        """
            Функция регистрации загружаемого модуля в список загруженных модулей приложения, для последующего быстрого доступа к ним из других модулей.

            :param name: Уникальное имя модуля
            :type name: String
            :param instance: Инициализированный класс модуля, откуда идет вызов
            :return: None
        """
        if name != "" and name != "Module":
            if name not in self.__register_modules:
                self.__register_modules[name] = instance
    
    
    def module_instance(self, name):
        """
            Функция возвращает инициализированный класс из списка загруженныйх модулей по точному совпадению имени.

            :param name: Уникальное имя загруженного модуля.
            :type name: String
            :return: Возвращает инициализированный модуль из списка загруженных
        """
        if name in self.__register_modules:
            return self.__register_modules[name]
        else:
            return None
    
    
    @staticmethod
    def module_request(name, check_only=False):
        """
            Функция возвращает обьект модуля, сохраненный в переменной запроса.

            :param name: Уникальное имя загруженного модуля.
            :type name: String
            :param check_only: Маркер вызова ошибки если данные в обькте запроса не найдены
            :type check_only: Boolean
            :return: Экземпляр класса :ref:`module-interfaces-web-module`
            :rtype: :ref:`module-interfaces-web-module`
        """
        module = getattr(request, '_4g_{}'.format(name.lower()), None)
        
        if module is None and check_only is False:
            abort(500)
        
        return module
    
    
    @staticmethod
    def module_request_save(name, instance):
        """
            Функция возвращает обьект модуля, сохраненный в переменной запроса.

            :param name: Уникальное имя загруженного модуля.
            :return: Экземпляр класса :ref:`module-interfaces-web-module`
            :rtype: :ref:`module-interfaces-web-module`
        """
        setattr(request, '_4g_{}'.format(name.lower()), instance)
    
    
    def module_exist(self, name):
        """
            Функция возвращает метку наличия загруженного модуля в системе по точному совпадению имени.

            :param name: Уникальное имя загруженного модуля.
            :type name: String
            :return: Возвращает метку наличия загруженного модуля в системе
            :rtype: Boolean
        """
        if name in self.__register_modules:
            return True
        else:
            return False
    
    
    def module_search(self, name, load_first=False):
        """
            Функция поиска загруженного модуля из списка загруженных.

            :param name: Уникальное имя загруженного модуля.
            :type name: String
            :param load_first: Если указано значение True, то функция возвращает инициализированный класс, иначе массив имен.
            :type load_first: Boolean
            :return: Возвращает инициализированный модуль из списка загруженных или один инициализированный класс.
        """
        module_names = []
        
        for module_name in self.__register_modules.keys():
            if module_name.find(name) == 0:
                if load_first:
                    return self.module_instance(module_name)
                
                module_names.append(module_name)
        
        if load_first:
            return None
        else:
            return module_names
    
    
    def send_static_file(self, filename):
        """
            Функция переопределения поиска статического файла изначально в папке сайте, далее в папке проекта. Если фаил и вовсе не был найден - выдаем ошибку 404.

            :param filename: Путь запрашеваемого статического файла
            :type filename: String
            :return:
        """
        if os.path.exists("{}/{}".format(self.__static_folder, filename)):
            return send_from_directory(self.__static_folder, filename)
        
        if os.path.exists("{}/{}".format(self.__static_folder_master, filename)):
            return send_from_directory(self.__static_folder_master, filename)
        
        return '', 404
    
    
    @locked_cached_property
    def jinja_loader(self):
        """
            Функция переопределения штатного загрузчика Flask, для поиска шаблона изначально в папке сайта а потом в папке проекта.

            :return: Экземпляр Jinja2 FileSystemLoader
        """
        return FileSystemLoader([self.__template_folder, self.__template_folder_master])


if __name__ == '__main__':
    # Подсветка выхлопа, только для дебага, что бы не засорять логи спец символами
    import Scopuli.Console.Logging.Colorer
    
    
    webapp = Application()
    
    webapp.run(threaded=True, host="0.0.0.0", port=5000)
