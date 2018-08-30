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


#
#   Базовый модуль "Ошибки"
#
#       Поставка: fG-Base
from Scopuli.WEB.Modules.Errors import WebError_400 as Error_400
from Scopuli.WEB.Modules.Errors import WebError_401 as Error_401
from Scopuli.WEB.Modules.Errors import WebError_404 as Error_404

#
#   Базовый модуль "Ядро"
#
#       Поставка: fG-Base
from Scopuli.WEB.Modules.Session import WebSession as Session
from Scopuli.WEB.Modules.Search import WebSearch as Search
from Scopuli.WEB.Modules.Account import WebAccount as Account
from Scopuli.WEB.Modules.Permissions import WebPermissions as Permissions
from Scopuli.WEB.Modules.Payment import WebPayment as Payment
from Scopuli.WEB.Modules.Cart import WebCart as Cart

from Scopuli.WEB.Modules.Pages import WebPage_Index as Page_Index
from Scopuli.WEB.Modules.Pages import WebPage_Simple as Page_Simple


#
#   Дополнительный модель "SEO Аналитика"
#
#       Поставка: fG-Base
from Scopuli.WEB.Modules.Sitemap import WebSitemap as Sitemap
from Scopuli.WEB.Modules.Robots import WebRobots as Robots

from Scopuli.WEB.Modules.Analytics import WebAnalytisc as Analytics


#
#   Дополнительные модели
#
#       Поставка: fG-Base
from Scopuli.WEB.Modules.Catalog import WebCatalog as Catalog
from Scopuli.WEB.Modules.Contacts import WebContacts as Contacts
from Scopuli.WEB.Modules.Vacancy import WebVacancy as Vacancy


#
#   Дополнительные модели: Костыли
#
#       Поставка: fG-Base
from Scopuli.WEB.Modules.Hooks.Favicon import WebFavicon as HookFavicon


#
#   Модуль "Блог"
#
#       Поставка: fG-Blog
from Scopuli.WEB.Modules.Blog import WebBlog as Blog
from Scopuli.WEB.Modules.Blog.Archive import WebBlogArchive as BlogArchive
from Scopuli.WEB.Modules.Blog.Post import WebBlogPost as BlogPost
from Scopuli.WEB.Modules.Blog.Posts import WebBlogPosts as BlogPosts
from Scopuli.WEB.Modules.Blog.Tag import WebBlogTag as BlogTag
from Scopuli.WEB.Modules.Blog.Tags import WebBlogTags as BlogTags


#
#   Модуль "Фитнес клуб"
#       Спонсор: ЦСД Амбассадор
#       Поставка: fG-Fitness
# from Scopuli.WEB.Modules.Club import WebClub as Club
# from Scopuli.WEB.Modules.Club.About import WebClubAbout as ClubAbout
# from Scopuli.WEB.Modules.Club.Schedule import WebClubSchedule as ClubSchedule
# from Scopuli.WEB.Modules.Club.Offers import WebClubOffers as ClubOffers
# from Scopuli.WEB.Modules.Club.Offer import WebClubOffer as ClubOffer
# from Scopuli.WEB.Modules.Club.Coachers import WebClubCoachers as ClubCoachers
# from Scopuli.WEB.Modules.Club.Coacher import WebClubCoacher as ClubCoacher
# from Scopuli.WEB.Modules.Club.Personal import WebClubPersonal as ClubPersonal
# from Scopuli.WEB.Modules.Club.Rooms import WebClubRooms as ClubRooms
# from Scopuli.WEB.Modules.Club.Room import WebClubRoom as ClubRoom
# from Scopuli.WEB.Modules.Club.Services import WebClubServices as ClubServices
# from Scopuli.WEB.Modules.Club.Service import WebClubService as ClubService
# from Scopuli.WEB.Modules.Club.Subscribe import WebClubSubscribe as ClubSubscribe


#
#   Модуль "Отель"
#       Спонсор: SPA Благодать
#       Поставка: fG-Hotel
# from Scopuli.WEB.Modules.Hotel import WebHotel as Hotel
# from Scopuli.WEB.Modules.Hotel.Rooms import WebHotelRooms as HotelRooms
# from Scopuli.WEB.Modules.Hotel.Room import WebHotelRoom as HotelRoom


#
#   Модуль "Магазин"
#       Спонсор: УчетЭнерго
#       Поставка: fG-ECommerce
# from Scopuli.WEB.Modules.Shop import WebShop as WebShop
# from Scopuli.WEB.Modules.Shop.Subsidiarys import WebShopSubsidiarys as ShopSubsidiarys
# from Scopuli.WEB.Modules.Shop.Subsidiary import WebShopSubsidiary as ShopSubsidiary
# from Scopuli.WEB.Modules.Shop.Groups import WebShopGroups as ShopGroups
# from Scopuli.WEB.Modules.Shop.Group import WebShopGroup as ShopGroup
# from Scopuli.WEB.Modules.Shop.Product import WebShopProduct as ShopProduct

