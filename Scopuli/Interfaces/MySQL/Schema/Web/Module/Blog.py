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
 
 
class WebModuleBlogTag(Base, Schema):
    """
        Таблица тэгов, модуля WebBlog
    """
    __tablename__ = 'web_module_blog_tag'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица тэгов, модуля WebBlog'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")

    url = Column(String(128), ColumnDefault(""), nullable=False, doc="Наименование в ASCII")
    name = Column(String(64), ColumnDefault(""), nullable=False, doc="Наименование")
    
    description = Column(String(64), ColumnDefault(""), nullable=False, doc="Описание тега")
    
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    
    frequency = Column(Integer(), ColumnDefault(1), index=True, nullable=False, doc="Частота использования")
    order = Column(Integer(), ColumnDefault(1), index=True, nullable=False, doc="Порядок сортировки")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")


class WebModuleBlogPostTag(Base, Schema):
    """
        Таблица связи тэгов и публикаций
    """
    __tablename__ = 'web_module_blog_post_tag'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица связи тэгов и публикаций'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_blog_post = Column(Integer(), ForeignKey('web_module_blog_post.id'), index=True, nullable=False, doc="Ссылка на WebBlogPost")
    cd_web_blog_tag = Column(Integer(), ForeignKey('web_module_blog_tag.id'), index=True, nullable=False, doc="Ссылка на WebBlogTag")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")

    # RelationShip's
    tag = relationship("WebModuleBlogTag")
    post = relationship("WebModuleBlogPost")


class WebModuleBlogPost(Base, Schema):
    """
        Таблица публикаций
    """
    __tablename__ = 'web_module_blog_post'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица публикаций'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_user = Column(Integer(), ForeignKey(User.id), nullable=False, doc="Ссылка на User, автора")
    
    title = Column(String(128), ColumnDefault(""), nullable=False, doc="Заголовок публикации")
    keywords = Column(String(128), ColumnDefault(""), nullable=False, doc="Ключевые слова публикации")
    type = Column(String(64), ColumnDefault(""), nullable=False, doc="Тип публикации")
    url = Column(String(128), ColumnDefault(""), nullable=False, doc="Уникальный URL публикации в ASCII")
    
    post_preview = Column(Text(), ColumnDefault(""), nullable=False, doc="Превью публикации в Markdown")
    post_full = Column(Text(), ColumnDefault(""), nullable=False, doc="Вся публикация в Markdown")
    
    is_draft = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка черновика")
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    is_snipped = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка привязки к шапке")
    
    date_published = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="Время создания записи, публикуемое")
    date_edited = Column(DateTime(), nullable=True, doc="Время изменение записи, публикуемое")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")

    # RelationShip's
    user = relationship(User)
    images = relationship("WebModuleBlogPostImage")
    tags = relationship("WebModuleBlogPostTag")
    files = relationship("WebModuleBlogPostFile")


class WebModuleBlogPostImage(Base, Schema):
    """
        Таблица связей публикации и изображений
    """
    __tablename__ = 'web_module_blog_post_image'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица связей публикации и изображений'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_blog_post = Column(Integer(), ForeignKey('web_module_blog_post.id'), index=True, nullable=False, doc="Ссылка на WebBlogPost")
    cd_image = Column(Integer(), ColumnDefault(1), ForeignKey(Image.id), nullable=False, doc="Ссылка на Image")
    
    order = Column(Integer(), ColumnDefault(1), nullable=False, doc="Порядковый номер")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание фотографии")
    alternate = Column(String(256), ColumnDefault(""), nullable=False, doc="Альтернативное имя фотографии")
    
    is_primary = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Метка обложки публикации")
    is_gallary = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Метка использования в галереи")
    is_article = Column(Boolean(), ColumnDefault(False), nullable=False, doc="Метка использования в теле публикации")
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")

    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")

    # RelationShip's
    post = relationship("WebModuleBlogPost")
    image = relationship(Image)


class WebModuleBlogPostFile(Base, Schema):
    """
        Таблица связей публикации и файлов
    """
    __tablename__ = 'web_module_blog_post_file'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица связей публикации и файлов'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_blog_post = Column(Integer(), ForeignKey('web_module_blog_post.id'), index=True, nullable=False, doc="Ссылка на WebBlogPost")
    cd_file = Column(Integer(), ColumnDefault(1), ForeignKey(File.id), nullable=False, doc="Ссылка на File")
    
    order = Column(Integer(), ColumnDefault(1), nullable=False, doc="Порядковый номер")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание файла")
    
    is_published = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка публикации")
    is_deleted = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")

    # RelationShip's
    post = relationship("WebModuleBlogPost")
    file = relationship(File)


class WebModuleBlogPostFileStatistic(Base, Schema):
    """
        Таблица со статистикой скачивания файла
    """
    __tablename__ = 'web_module_blog_post_file_statistic'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица со статистикой скачивания файла'
        }

    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_blog_post = Column(Integer(), ForeignKey('web_module_blog_post.id'), index=True, nullable=False, doc="Ссылка на WebBlogPost")
    cd_web_blog_post_file = Column(Integer(), ForeignKey('web_module_blog_post_file.id'), index=True, nullable=False,
                                   doc="Ссылка на WebBlogPostFile")
    cd_file = Column(Integer(), ColumnDefault(1), ForeignKey(File.id), nullable=False, doc="Ссылка на File")
    cd_user = Column(Integer(), ForeignKey(User.id), nullable=True, doc="Ссылка на User, скачавщего фаил")
    
    user_agent = Column(String(256), ColumnDefault(""), nullable=False, doc="Agent пользователя")
    user_ip = Column(String(32), ColumnDefault(""), nullable=False, doc="IP адрес пользователя")
    user_parms = Column(String(512), ColumnDefault(""), nullable=False, doc="Дополнительные данные сессии")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")
    
    # RelationShip's
    post = relationship("WebModuleBlogPost")
    file = relationship(File)


class WebModuleBlogPostStatistic(Base, Schema):
    """
        Таблица со статистикой публикации
    """
    __tablename__ = 'web_module_blog_post_statistic'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица со статистикой публикации'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_web_site = Column(Integer(), ForeignKey(WebSite.id), index=True, nullable=False, doc="Ссылка на WebSite")
    cd_web_blog_post = Column(Integer(), ForeignKey('web_module_blog_post.id'), index=True, nullable=False, doc="Ссылка на WebBlogPost")
    cd_user = Column(Integer(), ForeignKey(User.id), nullable=True, doc="Ссылка на User")
    
    is_like = Column(Integer(), ColumnDefault(0), nullable=False, doc="Счетсчик лайков")
    is_dislike = Column(Integer(), ColumnDefault(0), nullable=False, doc="Счетсчик дизлайков")
    is_visible = Column(Integer(), ColumnDefault(0), nullable=False, doc="Счетсчик просмотров")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(), doc="AutoLogger - Время последнего изменения")

    # RelationShip's
    post = relationship("WebModuleBlogPost")
