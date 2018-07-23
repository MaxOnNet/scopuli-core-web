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

from Scopuli.Interfaces.MySQL.Schema import Base
from Scopuli.Interfaces.MySQL.Schema.Core import File, Image
from Scopuli.Interfaces.MySQL.Schema.Core.User import User
from Scopuli.Interfaces.MySQL.Schema.Web import WebSite, WebPage


class WebModuleCart(Base, Schema):
    __tablename__ = 'web_module_cart'
    __table_args__ = \
        {'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': ''
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на сайт")
    cd_web_session = Column(Integer(), ForeignKey('web_module_session.id'), nullable=False, doc="Ссылка на уникальную сессию")
    cd_web_payment = Column(Integer(), ForeignKey('web_module_payment.id'), nullable=True, doc="Ссылка на платежный элемент")
    
    cd_user = Column(Integer(), ForeignKey(User.id), nullable=True, doc="Ссылка на пользователя")
    
    name = Column(String(128), ColumnDefault(""), nullable=False, doc="Название товара")
    description = Column(String(128), ColumnDefault(""), nullable=False, doc="Описание товара")
    count = Column(Integer(), ColumnDefault(0), nullable=False, doc="Количество элементов")
    price = Column(Float(), ColumnDefault(0), nullable=False, doc="Цена за 1 еденицу")
    amount = Column(Float(), ColumnDefault(0), nullable=False, doc="Сумма к оплате")
    
    object_id = Column(Integer(), ColumnDefault(0), nullable=False, doc="Идентификатор обьекта")
    object_type = Column(String(128), ColumnDefault(""), nullable=False, doc="Тип обьекта")
    object_url = Column(String(128), ColumnDefault(""), nullable=False, doc="Ссылка на обьект")
    object_image = Column(String(128), ColumnDefault(""), nullable=False, doc="Изображение обьекта")
    object_parm = Column(String(256), ColumnDefault(""), nullable=False, doc="Характеристики обьекта")
    
    is_editable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp())
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

