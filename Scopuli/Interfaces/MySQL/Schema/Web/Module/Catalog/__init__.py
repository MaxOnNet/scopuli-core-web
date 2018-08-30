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


class WebModuleCatalog(Base, Schema):
    """
        Таблица с данными каталога
    """
    __tablename__ = 'web_module_catalog'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с данными каталога'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_parent = Column(Integer(), ForeignKey('web_module_catalog.id'), nullable=True, doc="Родитель")
    
    title = Column(String(128), ColumnDefault(""), nullable=False, doc="Заголовок")
    url = Column(String(128), ColumnDefault(""), nullable=False, doc="Уникальный URL каталога в ASCII")
    
    text_preview = Column(Text(), ColumnDefault(""), nullable=False, doc="Превью описания каталога в Markdown")
    text_full = Column(Text(), ColumnDefault(""), nullable=False, doc="Полное описание каталога в Markdown")
    
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    use_price = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Показывать цену?")
    use_mark = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Использовать марку?")
    
    price_amount = Column(Integer(), ColumnDefault(0), nullable=False, doc="Цена")
    price_currency = Column(String(10), ColumnDefault(""), nullable=False, doc="Валюта")
    
    mark_label = Column(String(48), ColumnDefault(""), nullable=False, doc="Название метки")
    
    meta_title = Column(String(256), ColumnDefault(""), nullable=False, doc="Заголовок страницы")
    meta_description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание страницы")
    meta_keywords = Column(String(256), ColumnDefault(""), nullable=False, doc="Ключевые слова")
    
    # Automatic Logger
    date_published = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="Время создания записи, публичное")
    date_edited = Column(DateTime(), nullable=True, doc="Время изменение записи, публичное")
    
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")
    
    # RelationShip's
    parent = relationship("WebModuleCatalog", remote_side=[id])
    images = relationship("WebModuleCatalogImage")


class WebModuleCatalogImage(Base, Schema):
    """
        Таблица связей каталога и изображений
    """
    __tablename__ = 'web_module_catalog_image'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица связей каталога и изображений'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_catalog = Column(Integer(), ForeignKey('web_module_catalog.id'), index=True, nullable=False, doc="Ссылка на WebModuleCatalog")
    cd_image = Column(Integer(), ColumnDefault(1), ForeignKey(Image.id), nullable=False, doc="Ссылка на Image")
    
    order = Column(Integer(), ColumnDefault(1), nullable=False, doc="Порядковый номер")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание фотографии")
    alternate = Column(String(256), ColumnDefault(""), nullable=False, doc="Альтернативное имя фотографии")
    
    is_primary = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Использовать как исновное")
    is_gallary = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Использовать в галереи внизу страницы")
    is_article = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Изображение используется в теле страницы")
    is_published = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Опубликовано ли изображение")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")
    
    # RelationShip's
    catalog = relationship("WebModuleCatalog")
    image = relationship(Image)
