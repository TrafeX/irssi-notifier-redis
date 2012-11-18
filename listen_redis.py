#!/usr/bin/env python
#
# Irssi notifier using Redis
#
# Copyright (c) 2012, Tim de Pater <code AT trafex DOT nl>
# <https://github.com/TrafeX/irssi-notifier-redis>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import sys
import dbus
import redis
import threading
import config

class ListenThread(threading.Thread):
    def __init__(self):
        self.bus = False
        self.notifyservice = False
        self.notifyid = 0
        threading.Thread.__init__(self)
        self.setDaemon(False)

    def run(self):
        print threading.currentThread().getName(), 'Starting'
        r = redis.StrictRedis(
                host=config.redis['server'],
                port=config.redis['port'],
                password=config.redis['password'],
                db=0
            )

        ps = r.pubsub()
        ps.subscribe(['irssi'])

        for item in ps.listen():
            print item
            msg = str(item['data']).partition('  ')
            if item['type'] == 'message' and len(msg[2]) > 0:
                self.notify(msg[0], msg[2])
        print threading.currentThread().getName(), 'Exiting'

    def notify(self, channel, msg):
        self.bus = dbus.Bus(dbus.Bus.TYPE_SESSION)
        # Connect to notification interface on DBUS.
        self.notifyservice = self.bus.get_object(
            'org.freedesktop.Notifications',
            '/org/freedesktop/Notifications'
        )
        self.notifyservice = dbus.Interface(
            self.notifyservice,
            "org.freedesktop.Notifications"
        )
        # The second param is the replace id, so get the notify id back,
        # store it, and send it as the replacement on the next call.
        self.notifyservice.Notify(
            "Irssi-notify",
            self.notifyid,
            sys.path[0] + "/icon-irc.png",
            channel,
            msg,
            [],
            {},
            5000
        )

if __name__ == '__main__':
    try:
        thread = ListenThread()
        thread.start();

    except ValueError as strerror:
        print strerror
    except KeyboardInterrupt:
        print "\nStopping monitor..\n"
        sys.exit(0)
    except:
        raise
