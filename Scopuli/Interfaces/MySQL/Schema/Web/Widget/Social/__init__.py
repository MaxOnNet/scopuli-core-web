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

from Scopuli.Interfaces.MySQL.Schema.Web.Core import WebSite


class WebWidgetSocialType(Base, Schema):
    """
        Таблица с типами данных виджета Social
    """
    __tablename__ = 'web_widget_social_type'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с типами данных виджета Social'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    
    code = Column(String(64), ColumnDefault(""), nullable=False, doc="Кодовое наименование")
    name = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование")
    
    description = Column(String(64), ColumnDefault(""), nullable=False, doc="Описание")
    
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")


class WebWidgetSocial(Base, Schema):
    """
        Таблица данных виджета Social
    """
    __tablename__ = 'web_widget_social'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица данных виджета Social'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_widget_social_type = Column(Integer(), ForeignKey('web_widget_social_type.id'), index=True, nullable=False,
                                       doc="Ссылка на WebWidgetSocialType")
    
    url = Column(String(128), ColumnDefault(""), nullable=False, doc="URL социальной сети в ASCII")
    name = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование социальной сети")
    
    description = Column(String(64), ColumnDefault(""), nullable=False, doc="Описание социальной сети")
    
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")
    order = Column(Integer(), ColumnDefault(1), index=True, nullable=False, doc="Порядок сортировки")
    
    # RelationShip's
    site = relationship(WebSite, backref="WebWidgetSocial")
    type = relationship("WebWidgetSocialType", backref="WebWidgetSocial")
