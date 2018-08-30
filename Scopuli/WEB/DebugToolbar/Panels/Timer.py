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


import resource
import time

from Scopuli.WEB.DebugToolbar.Panels import DebugPanel

_ = lambda x: x


class TimerDebugPanel(DebugPanel):
    """
    Panel that displays the time a response took in milliseconds.
    """
    
    name = 'Timer'
    has_content = True
    has_resource = True

    def process_request(self, request):
        self._start_time = time.time()
        self._start_rusage = resource.getrusage(resource.RUSAGE_SELF)

    def process_response(self, request, response):
        self.total_time = (time.time() - self._start_time) * 1000
        self._end_rusage = resource.getrusage(resource.RUSAGE_SELF)

    def nav_title(self):
        return _('Время выболнения')

    def nav_subtitle(self):
        return 'Всего: %0.2fms' % (self.total_time)

        utime = self._end_rusage.ru_utime - self._start_rusage.ru_utime
        stime = self._end_rusage.ru_stime - self._start_rusage.ru_stime
        
        return 'CPU: %0.2fms (%0.2fms)' % (
               (utime + stime) * 1000.0, self.total_time)

    def title(self):
        return _('Использование ресурсов')

    def url(self):
        return ''

    def _elapsed_ru(self, name):
        return (getattr(self._end_rusage, name)
                - getattr(self._start_rusage, name))

    def content(self):
        utime = 1000 * self._elapsed_ru('ru_utime')
        stime = 1000 * self._elapsed_ru('ru_stime')
        vcsw = self._elapsed_ru('ru_nvcsw')
        ivcsw = self._elapsed_ru('ru_nivcsw')
        minflt = self._elapsed_ru('ru_minflt')
        majflt = self._elapsed_ru('ru_majflt')

        blkin = self._elapsed_ru('ru_inblock')
        blkout = self._elapsed_ru('ru_oublock')
        swap = self._elapsed_ru('ru_nswap')
        rss = self._end_rusage.ru_maxrss
        srss = self._end_rusage.ru_ixrss
        urss = self._end_rusage.ru_idrss
        usrss = self._end_rusage.ru_isrss
        
        rows = (
            (_('User CPU time'), '%0.3f msec' % utime),
            (_('System CPU time'), '%0.3f msec' % stime),
            (_('Total CPU time'), '%0.3f msec' % (utime + stime)),
            (_('Elapsed time'), '%0.3f msec' % self.total_time),
            (_('Context switches'), '%d voluntary, %d involuntary' % (vcsw, ivcsw)),
            (_('Memory use'), '%d max RSS, %d shared, %d unshared' % (rss, srss, urss + usrss)),
            (_('Page faults'), '%d no i/o, %d requiring i/o' % (minflt, majflt)),
            (_('Disk operations'), '%d in, %d out, %d swapout' % (blkin, blkout, swap))
        )

        context = self.context.copy()
        context.update({
            'rows': rows,
        })

        return self.render('panels/timer.html', context)
