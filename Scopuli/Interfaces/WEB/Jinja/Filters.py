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

import phonenumbers

def _decode_text(value):
    """
        Decode a text-like value for display.

        Unicode values are returned unchanged. Byte strings will be decoded
        with a text-safe replacement for unrecognized characters.
    """
    if isinstance(value, bytes):
        return value.decode('ascii', 'replace')
    else:
        return value


def filter_markdown(value):
    from flask import Markup
    from markdown import markdown
    
    return Markup(markdown(value))


def filter_printable(value):
    try:
        return _decode_text(repr(value))
    except Exception as e:
        return '<repr(%s) raised %s: %s>' % (
               object.__repr__(value), type(e).__name__, e)


def filter_shuffle(seq):
    import random
    
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq


def filter_phonenumber(value, country='RU', format=phonenumbers.PhoneNumberFormat.INTERNATIONAL):
    try:
        parsed = phonenumbers.parse(value, country)
        return phonenumbers.format_number(parsed, format)
    except phonenumbers.NumberParseException as e:
        return value


def filter_money(value):
    return "{money:0,.2f} р.".format(money=value)