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

from Scopuli.Interfaces.MySQL.Schema.Web.Core import WebSite, WebPage


class WebWidgetMenu(Base, Schema):
    """
        Таблица с данными виджета Menu
    """
    __tablename__ = 'web_widget_menu'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с данными виджета Menu'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_page = Column(Integer(), ForeignKey(WebPage.id), index=True, nullable=False, doc="Ссылка на WebPage")
    cd_parent = Column(Integer(), ForeignKey(id), nullable=True, doc="Родитель")
    
    type = Column(String(32), ColumnDefault("main"), nullable=False, doc="Тип меню: top | main | footer")
    
    target = Column(String(32), ColumnDefault("_self"), nullable=False, doc="Значение аттрибуда ``target`` тега ``a``")
    
    css_class_lg = Column(String(32), ColumnDefault(""), nullable=False, doc="Имя класса CSS тега ``data-class-lg``")
    css_class_md = Column(String(32), ColumnDefault(""), nullable=False, doc="Имя класса CSS тега ``data-class-md``")
    css_class_sm = Column(String(32), ColumnDefault(""), nullable=False, doc="Имя класса CSS тега ``data-class-sm``")
    css_class_xs = Column(String(32), ColumnDefault(""), nullable=False, doc="Имя класса CSS тега ``data-class-xs``")
    css_class_xxs = Column(String(32), ColumnDefault(""), nullable=False, doc="Имя класса CSS тега ``data-class-xss``")
    
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Матка использования")
    order = Column(Integer(), ColumnDefault(1), index=True, nullable=False, doc="Порядок сортировки")
    
    # RelationShip's
    parent = relationship("WebWidgetMenu", remote_side=[id])
    site = relationship(WebSite, backref="WebWidgetMenu")
    page = relationship(WebPage, backref="WebWidgetMenu")
