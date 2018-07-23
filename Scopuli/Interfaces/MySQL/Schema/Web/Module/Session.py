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

from Interfaces.MySQL.SQLAlchemy import *

from Interfaces.MySQL.Schema import Base
from Interfaces.MySQL.Schema.Core import File, Image
from Interfaces.MySQL.Schema.Core.User import User
from Interfaces.MySQL.Schema.Club import Club
from Interfaces.MySQL.Schema.Web import WebSite, WebPage
import json


class WebModuleSession(Base, Schema):
    """
        Таблица с перечнем пользовательских сессий
    """
    __tablename__ = 'web_module_session'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с перечнем пользовательских сессий'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_page = Column(Integer(), ForeignKey(WebPage.id), nullable=True, doc="Ссылка на WebPage")
    
    cd_user = Column(Integer(), ForeignKey(User.id), nullable=True, doc="Ссылка на User")
    cd_club = Column(Integer(), ForeignKey(Club.id), nullable=True, doc="Ссылка на Club")
    
    request_url = Column(String(256), ColumnDefault(""), nullable=False, doc="URL текущей страницы")
    
    user_agent = Column(String(256), ColumnDefault(""), nullable=False, doc="Agent пользователя")
    user_ip = Column(String(32), ColumnDefault(""), nullable=False, doc="IP адрес пользователя")
    user_parms = Column(Text(2048), ColumnDefault(""), nullable=False, doc="Дополнительные данные сессии")
    
    # Automatic Logger
    date_active = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последней активности")
    date_login = Column(DateTime(), nullable=True, doc="AutoLogger - Время авторизации")
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")

    #: Преобразованное поле UserParms в JSON Object
    __user_parms_json = None
    
    def __user_parms_load(self):
        """
            Функция загрузки обьекта из строкового значения извлеченного из БД
        :return:
        """
        if self.__user_parms_json is None:
            if self.user_parms == "":
                self.user_parms = "{}"
        
            self.__user_parms_json = json.loads(self.user_parms)


    def __user_parms_save(self):
        """
            Функция упаковки обьекта в строковое значение с последующей записью в БД
            :return: Nothing
        """
        if self.__user_parms_json is not None:
            self.user_parms = json.dumps(self.__user_parms_json)


    def get_property(self, name, default=None):
        """
            Функция получения данных из БД
            
            :param name: Название ппараметра
            :type name: String
            :param default: Значение по умолчанию, если значение не найдено в БД
            :type default: Any
            :return: Сохраненное значение or default
            :rtype: String or default type
        """
        self.__user_parms_load()
        
        if name in self.__user_parms_json:
            return self.__user_parms_json[name]
        
        return default

    def set_property(self, name, value):
        """
            Функция записи данных БД
            
            :param name: Название ппараметра
            :type name: String
            :param value: Сохраняемое значение
            :type value: String
            :return: Nothing
            :rtype: Nothing
        """
        self.__user_parms_load()
        self.__user_parms_json[name] = value
        self.__user_parms_save()
