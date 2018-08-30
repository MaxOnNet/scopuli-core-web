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

from Scopuli.Interfaces.MySQL.SQLAlchemy import *

from Scopuli.Interfaces.MySQL.Schema.Core import File, Image
from Scopuli.Interfaces.MySQL.Schema.Web.Core import WebSite, WebPage


class WebModuleVacancy(Base, Schema):
    """
        Таблица с данными о вакансиях
    """
    __tablename__ = 'web_module_vacancy'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с данными о вакансиях'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_page = Column(Integer(), ForeignKey(WebPage.id), index=True, nullable=False, doc="Ссылка на WebPage")
    
    title = Column(String(128), ColumnDefault(""), nullable=False, doc="Наименование вакансии")
    description = Column(String(1024), ColumnDefault(""), nullable=False, doc="Описание вакансии")
    
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    order = Column(Integer(), ColumnDefault(1), index=True, nullable=False, doc="Порядок сортировки")
    
    requirements = Column(String(1024), ColumnDefault(""), nullable=False, doc="Требования")
    expectations = Column(String(1024), ColumnDefault(""), nullable=False, doc="Чего мы ожидаем")
    reward = Column(String(1024), ColumnDefault(""), nullable=False, doc="Чего Вы получите")
