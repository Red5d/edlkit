#!/usr/bin/env python

"""Stopwatch, a portable multi-lap timing utility class.
Copyright (C) 2006  George F. Rice

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import time

class stopwatch:
  """ Implements a timer with multiple named lap timers.
      A newly created timer is NOT running.
      Use start() and stop() to begin/end. Check boolean '.running'.
      A lap timer is created on reference.
  """
  def __init__(self, name = "stopwatch"):
    self.name = name
    self.startTime = time.time()
    self.elapsedTime = 0.0
    self.running = False
    self.lap = {}

  def start(self):
    """ Start or restart the timer.
        Note that while the timer is running,
        only the getElapsedTime() method is accurate
        for determining elapsed time.
    """
    if not self.running:
        self.startTime = time.time()
        self.running = True

  def stop(self):
    """ Stop the timer and update the elapsedTime attribute.
    """
    if self.running:
        self.elapsedTime += time.time() - self.startTime
        self.running = False

  def getElapsedTime(self):
    """ Returns the elapsed time as a float in seconds,
        regardless of the state of the timer.
    """
    if self.running:
        return self.elapsedTime + (time.time() - self.startTime)
    else:
        return self.elapsedTime

  def stopLapTimer(self, lap = "lap timer"):
    """ Set (or reset) the named (or default) lap timer
        to the current elapsed time.  The lap time is returned.
    """
    self.lap[lap] = self.getElapsedTime()
    return self.lap[lap]

  def getLapTime(self, lap = "lap timer"):
    """ Return the named (or default) lap time.  If it doesn't exist,
        it is created as the current elapsed time.
    """
    try:
        return self.lap[lap]
    except:
        self.lap[lap] = self.getElapsedTime()
        return self.lap[lap]

  def getFormattedTime(self, lap = None):
    """ Return specified lap time (or elapsed time if omitted)
        formatted as HH:MM:SS.ds
    """
    if lap == None:
      _et = self.getElapsedTime()
    else:
      _et = self.getLapTime(lap)
    _et += 0.005   # round to nearest hundredth
    _hh = int(_et / 3600)
    _et -= (_hh * 3600)
    _mm = int(_et / 60)
    _et -= (_mm * 60)
    _ss = int(_et)
    _et -= _ss
    _ds = int(_et * 100)
    return "%.2d:%.2d:%.2d.%.2d" % (_hh, _mm, _ss, _ds)
