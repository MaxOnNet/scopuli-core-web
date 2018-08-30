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

from Scopuli.Interfaces.MySQL.SQLAlchemy import *

from Scopuli.Interfaces.MySQL.Schema.Core.Server import Server


class WebSite(Base, Schema):
    """
        Таблица с перечнем сайтов
    """
    __tablename__ = 'web_site'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с перечнем сайтов'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_server = Column(Integer(), ColumnDefault(2021), ForeignKey(Server.id), default=2020, nullable=False, doc="Ссылка на Server")
    
    code = Column(String(64), ColumnDefault(""), nullable=False, doc="Уникальный код сайта в ASCII")
    url = Column(String(64), ColumnDefault(""), nullable=False, doc="Уникальный URL сайта в ASCII")
    
    code_develop = Column(String(64), ColumnDefault(""), nullable=False, doc="Уникальный код сайта в ASCII для разработки")
    url_develop = Column(String(64), ColumnDefault(""), nullable=False, doc="Уникальный URL сайта в ASCII для разработки")
    
    title = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование")
    description = Column(String(128), ColumnDefault(""), nullable=False, doc="Описание")
    
    meta_title = Column(String(256), ColumnDefault(""), nullable=False, doc="Заголовок сайта")
    meta_description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание сайта")
    meta_autor = Column(String(256), ColumnDefault(""), nullable=False, doc="Автор сайта")
    meta_autor_url = Column(String(64), ColumnDefault(""), nullable=False, doc="Адрес автора сайта")
    meta_keywords = Column(String(256), ColumnDefault(""), nullable=False, doc="Перечень ключевых слов")
    meta_copyrights = Column(String(256), ColumnDefault(""), nullable=False, doc="Копирайтинг")
    
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")
    is_secure = Column(Boolean(), ColumnDefault(False), default=True, nullable=False, doc="Метка использования SSL")
    is_devel = Column(Boolean(), ColumnDefault(False), default=True, nullable=False, doc="Метка статуса сайта")
    
    # RelationShip's
    pages = relationship("WebPage", lazy='dynamic')
    
    server = relationship(Server, backref='WebPage')
    
    
    @hybrid_property
    def ip_port(self):
        """
            Возвращает номер порта сервера на котором располоден виртуальный хост.

            :return: Номер порта
            :rtype: Integer
        """
        if self.is_secure:
            return 443
        else:
            return 80
    
    
    @hybrid_property
    def ip_addr(self):
        """
            Возвращает IP адрес сервера на котором расположен виртуальный хост.

            :return: IP адрес сервера
            :rtype: IPAddress
        """
        return self.server.address_ipv4
    
    
    @hybrid_property
    def url_prefix(self):
        """
            Возвращает префикс протокола по которому работает данный сайт.

            :return: Url prefix Http or Https
            :rtype: String
        """
        if self.is_secure:
            return "https://"
        else:
            return "http://"


class WebPage(Base, Schema):
    """
        Таблица с перечнем страниц
    """
    __tablename__ = 'web_page'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с перечнем страниц'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey('web_site.id'), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_parent = Column(Integer(), ForeignKey(id), nullable=True, doc="Родитель")
    
    code = Column(String(64), ColumnDefault(""), nullable=False, doc="Кодовое наименование модуля в ASCII")
    
    title = Column(String(128), ColumnDefault(""), nullable=False, doc="Наименование страницы")
    description = Column(String(128), ColumnDefault(""), nullable=False, doc="Описание страницы")
    
    url = Column(String(64), ColumnDefault(""), nullable=False, doc="Уникальный URL модуля в ASCII")
    url_title = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование ссылки")
    url_title_short = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование ссылки короткое")
    url_description = Column(String(128), ColumnDefault(""), nullable=False, doc="Описание ссылки")
    url_description_short = Column(String(128), ColumnDefault(""), nullable=False, doc="Описание ссылки короткое")
    
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")
    
    template_name = Column(String(256), ColumnDefault(""), nullable=False, doc="Название шаблона")
    
    meta_title = Column(String(256), ColumnDefault(""), nullable=False, doc="Заголовок страницы")
    meta_description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание страницы")
    meta_autor = Column(String(256), ColumnDefault(""), nullable=False, doc="Автор страницы")
    meta_autor_url = Column(String(64), ColumnDefault(""), nullable=False, doc="Адрес автора страницы")
    meta_keywords = Column(String(256), ColumnDefault(""), nullable=False, doc="Перечень ключевых слов")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")
    
    # RelationShip's
    parent = relationship("WebPage", remote_side=[id])
    site = relationship("WebSite", backref="WebPage")
