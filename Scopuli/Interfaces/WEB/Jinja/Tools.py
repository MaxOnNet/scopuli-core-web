#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [20187] Tatarnikov Viktor [viktor@tatarnikov.org]
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

import calendar

from jinja2 import nodes
from jinja2.ext import Extension

from flask.json import JSONEncoder

from datetime import datetime


def parse(data):
    result = {}
    for line in data.splitlines():
        if ':' in line:
            key, value = parse_line(line)
            result[key] = value
    return result


def parse_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def parse_line(line):
    key, value = strip(line.split(':', 1))
    s, e = value.startswith, value.endswith
    if s('[') and e(']'):
        value = strip(value[1:-1].split(','))
    elif s('{') and e('}'):
        value = dict(strip(x.split(':')) for x in value[1:-1].split(','))
    elif s('date:'):
        value = parse_date(value[len('date:'):].strip())
    elif key.strip() == 'date':
        try:
            value = parse_date(value)
        except ValueError:
            pass
    elif value.lower() in 'true yes on'.split():
        value = True
    elif value.lower() in 'false no off'.split():
        value = False
    return key, value


def strip(lst):
    return [x.strip() for x in lst]


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
                return millis
            
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
    