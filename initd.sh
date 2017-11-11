#!/bin/bash
### BEGIN INIT INFO
# Provides:          hook-bot
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Hook bot at boot time
# Description:       Enable hook bot
### END INIT INFO

# Daemon init script of the docker demo site
# Copyright (C) 2016  Marcos Zuriaga Miguel <wolfi at wolfi.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

NAME=hook-bot

RUNDIR=/var/run
PIDFILE=$RUNDIR/hook-bot.pid

DAEMON=DAEMON_PATH
DAEMON_ARGS="daemon pidfile $PIDFILE"

case "$1" in
  start)
	echo -n "Starting $DESC: "
	mkdir -p $RUNDIR
	touch $PIDFILE
	chown root:root $PIDFILE

	if start-stop-daemon --start --oknodo --background --pidfile $PIDFILE --chuid root:root --exec $DAEMON -- $DAEMON_ARGS
	then
		echo "$NAME. Started"
	else
		echo "failed"
	fi
    ;;
  stop)
    echo -n "Stopping $NAME: "

	if [ -s $PIDFILE ]
	then
		kill $(pstree -p `cat $PIDFILE` | tr "\n" " " |sed "s/[^0-9]/ /g" |sed "s/\s\s*/ /g")
		echo "$NAME. Stopped"
	else
		echo "Failed to stop daemon, no such pid file, is daemon running?"
	fi

	rm -f $PIDFILE
    ;;
  restart|reload|force-reload)
    $0 stop
    sleep 1
    $0 start
    ;;
  status)
	status_of_proc -p ${PIDFILE} ${DAEMON} ${NAME}
    ;;
  *)
    echo "Usage: /etc/init.d/$NAME {start|stop|restart|force-reload|status}" >&2
	exit 1
esac