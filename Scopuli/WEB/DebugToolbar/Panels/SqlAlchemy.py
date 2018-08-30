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

#try:
#    from Interfaces.MySQL.SQLAlchemy import *
#    from flask_sqlalchemy import get_debug_queries, SQLAlchemy
#except ImportError:
#    sqlalchemy_available = False
#    get_debug_queries = SQLAlchemy = None
#else:
import sys
import time
import itsdangerous

from operator import itemgetter

from werkzeug.local import LocalProxy

from flask import request, current_app, abort, json_available, g

from WEB.DebugToolbar import module
from WEB.DebugToolbar.Panels import DebugPanel
from WEB.DebugToolbar.Utils import format_fname, format_sql



_ = lambda x: x

def _calling_context(app_path):
    frm = sys._getframe(1)
    while frm.f_back is not None:
        name = frm.f_globals.get('__name__')
        if name and (name == app_path or name.startswith(app_path + '.')):
            funcname = frm.f_code.co_name
            return '%s:%s (%s)' % (
                frm.f_code.co_filename,
                frm.f_lineno,
                funcname
            )
        frm = frm.f_back
    return '<unknown>'

class _DebugQueryTuple(tuple):
    statement = property(itemgetter(0))
    parameters = property(itemgetter(1))
    start_time = property(itemgetter(2))
    end_time = property(itemgetter(3))
    context = property(itemgetter(4))

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __repr__(self):
        return '<query statement="%s" parameters=%r duration=%.03f>' % (
            self.statement,
            self.parameters,
            self.duration
        )

class _EngineDebuggingSignalEvents(object):
    """Sets up handlers for two events that let us track the execution time of
    queries."""

    def __init__(self, engine, import_name):
        self.engine = engine
        self.app_package = import_name

    def register(self):
        from sqlalchemy import event
        
        event.listen(
            self.engine, 'before_cursor_execute', self.before_cursor_execute
        )
        event.listen(
            self.engine, 'after_cursor_execute', self.after_cursor_execute
        )

    def before_cursor_execute(
        self, conn, cursor, statement, parameters, context, executemany
    ):
        if current_app:
            context._query_start_time = time.time()

    def after_cursor_execute(
        self, conn, cursor, statement, parameters, context, executemany
    ):
        if current_app:
            if 'sqlalchemy_queries' not in g:
                g.sqlalchemy_queries = []

            g.sqlalchemy_queries.append(_DebugQueryTuple((
                statement, parameters, context._query_start_time, time.time(),
                _calling_context(self.app_package)
            )))


def query_signer():
    return itsdangerous.URLSafeSerializer(current_app.config['SECRET_KEY'],
                                          salt='fdt-sql-query')


def is_select(statement):
    prefix = b'select' if isinstance(statement, bytes) else 'select'
    return statement.lower().strip().startswith(prefix)


def dump_query(statement, params):
    if not params or not is_select(statement):
        return None

    try:
        return query_signer().dumps([statement, params])
    except TypeError:
        return None


def load_query(data):
    try:
        statement, params = query_signer().loads(request.args['query'])
    except (itsdangerous.BadSignature, TypeError):
        abort(406)

    # Make sure it is a select statement
    if not is_select(statement):
        abort(406)

    return statement, params


class SQLAlchemyDebugPanel(DebugPanel):
    """
    Panel that displays the time a response took in milliseconds.
    """
    name = 'SQLAlchemy'

    def process_request(self, request):
        if request.endpoint != "static":
            database = LocalProxy(current_app.database.request_get)
            _EngineDebuggingSignalEvents(database.bind, current_app.import_name).register()

    def process_response(self, request, response):
        pass

    @property
    def has_content(self):
        return True

    def nav_title(self):
        return _('SQLAlchemy')

    def nav_subtitle(self):
        count = len(g.get('sqlalchemy_queries', ()))

        if not count:
            return 'Unavailable'

        return '%d %s' % (count, 'query' if count == 1 else 'queries')

    def title(self):
        return _('SQLAlchemy queries')

    def url(self):
        return ''

    def content(self):
        queries = g.get('sqlalchemy_queries', ())

        if not queries:
            return self.render('panels/sqlalchemy_error.html', {
                'json_available': json_available,
            })

        data = []
        for query in queries:
            data.append({
                'duration': query.duration,
                'sql': format_sql(query.statement, query.parameters),
                'signed_query': dump_query(query.statement, query.parameters),
                'context_long': query.context,
                'context': format_fname(query.context)
            })
        return self.render('panels/sqlalchemy.html', {'queries': data})

# Panel views


@module.route('/sqlalchemy/sql_select', methods=['GET', 'POST'])
@module.route('/sqlalchemy/sql_explain', methods=['GET', 'POST'],
              defaults=dict(explain=True))
def sql_select(explain=False):
    statement, params = load_query(request.args['query'])
    engine = LocalProxy(current_app.database.request_get)

    if explain:
        if engine.driver == 'pysqlite':
            statement = 'EXPLAIN QUERY PLAN\n%s' % statement
        else:
            statement = 'EXPLAIN\n%s' % statement

    result = engine.execute(statement, params)
    return g.debug_toolbar.render('panels/sqlalchemy_select.html', {
        'result': result.fetchall(),
        'headers': result.keys(),
        'sql': format_sql(statement, params),
        'duration': float(request.args['duration']),
    })
