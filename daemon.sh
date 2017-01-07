#!/bin/bash
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

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

# Load configuration
source $SCRIPTPATH/daemon_config

# Sets up the autostart features on rc.d and init.d to launch the daemon on boot
function install_autostart() {
	# Copy the script to the init scripts
	cp $SCRIPTPATH/initd.sh /etc/init.d/github-telegram-bot

	# Insert absolute path to this file
	sed -i "s|DAEMON_PATH|$SCRIPT|g" /etc/init.d/github-telegram-bot

	# Enable rc.d autorun of the daemon
	update-rc.d github-telegram-bot defaults
	update-rc.d github-telegram-bot enable
}

# Runs the actual daemon and restarts it in case it fails
function daemon(){
    export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages:${SCRIPTPATH}"
	while (true);
	do
		python $SCRIPTPATH/webhooks.py
		sleep 2
	done
}

# Deletes the autostart from rc levels and init script
function remove_autostart() {
	rm /etc/init.d/github-telegram-bot
	update-rc.d github-telegram-bot remove
}

case "$1" in
	install)
		install_autostart
	;;
	daemon)
		case "$2" in
			pidfile)
				echo $$ > $3
			;;
		esac
		daemon
	;;
	uninstall)
		remove_autostart
	;;
	*)
		echo "usage: daemon.sh install|uninstall|daemon";
		echo "This script must be run as root!";
esac