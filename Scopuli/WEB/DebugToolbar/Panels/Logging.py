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
from __future__ import with_statement

import datetime
import logging
try:
    import threading
except ImportError:
    threading = None

from Scopuli.WEB.DebugToolbar.Panels import DebugPanel
from Scopuli.WEB.DebugToolbar.Utils import format_fname

_ = lambda x: x


class ThreadTrackingHandler(logging.Handler):
    def __init__(self):
        if threading is None:
            raise NotImplementedError("threading module is not available, \
                the logging panel cannot be used without it")
        logging.Handler.__init__(self)
        self.records = {}  # a dictionary that maps threads to log records

    def emit(self, record):
        self.get_records().append(record)

    def get_records(self, thread=None):
        """
        Returns a list of records for the provided thread, of if none is
        provided, returns a list for the current thread.
        """
        if thread is None:
            thread = threading.currentThread()
        if thread not in self.records:
            self.records[thread] = []
        return self.records[thread]

    def clear_records(self, thread=None):
        if thread is None:
            thread = threading.currentThread()
        if thread in self.records:
            del self.records[thread]


handler = None
_init_lock = threading.Lock()


def _init_once():
    global handler
    if handler is not None:
        return
    with _init_lock:
        if handler is not None:
            return

        # Call werkzeug's internal logging to make sure it gets configured
        # before we add our handler.  Otherwise werkzeug will see our handler
        # and not configure console logging for the request log.
        # Werkzeug's default log level is INFO so this message probably won't
        # be seen.
        try:
            from werkzeug._internal import _log
        except ImportError:
            pass
        else:
            _log('debug', 'Initializing forGain-DebugToolbar log handler')

        handler = ThreadTrackingHandler()
        logging.root.addHandler(handler)


class LoggingDebugPanel(DebugPanel):
    name = 'Logging'
    has_content = True

    def process_request(self, request):
        _init_once()
        handler.clear_records()

    def get_and_delete(self):
        records = handler.get_records()
        handler.clear_records()
        return records

    def nav_title(self):
        return _("Logging")

    def nav_subtitle(self):
        # FIXME l10n: use ngettext
        num_records = len(handler.get_records())
        return '%s message%s' % (num_records, '' if num_records == 1 else 's')

    def title(self):
        return _('Log Messages')

    def url(self):
        return ''

    def content(self):
        records = []
        for record in self.get_and_delete():
            records.append({
                'message': record.getMessage(),
                'time': datetime.datetime.fromtimestamp(record.created),
                'level': record.levelname,
                'file': format_fname(record.pathname),
                'file_long': record.pathname,
                'line': record.lineno,
            })

        context = self.context.copy()
        context.update({'records': records})

        return self.render('panels/logger.html', context)
