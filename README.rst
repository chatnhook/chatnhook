======================
Python GitHub Telegram Bot
======================

Sends notifications from github to telegram

Install
=======

::

    git clone https://github.com/brantje/telegram-github-bot.git
    cd telegram-github-bot


Dependencies
============

::

   sudo pip install -r requirements.txt


Setup
=====
You can configure what the application does by changing ``config.json``:

::

    {
        "github_ips_only": true,
        "enforce_secret": "",
        "return_scripts_info": true
        "hooks_path": "/.../hooks/",
        "telegram_token": "241059146:AAHcsVPudn1o_B8-RMSa1miNHUGcxQySPVQ",
        "server_url": "https://webhook.passman.cc",
        "notify_branches": ["master"]
    }

:github_ips_only: Restrict application to be called only by GitHub IPs. IPs
 whitelist is obtained from
 `GitHub Meta <https://developer.github.com/v3/meta/>`_
 (`endpoint <https://api.github.com/meta>`_). Default: ``true``.
:enforce_secret: Enforce body signature with HTTP header ``X-Hub-Signature``.
 See ``secret`` at
 `GitHub WebHooks Documentation <https://developer.github.com/v3/repos/hooks/>`_.
 Default: ``''`` (do not enforce).
:return_scripts_info: Return a JSON with the ``stdout``, ``stderr`` and exit
 code for each executed hook using the hook name as key. If this option is set
 you will be able to see the result of your hooks from within your GitHub
 hooks configuration page (see "Recent Deliveries").
 Default: ``true``.
:hooks_path: Configures a path to import the hooks. If not set, it'll import
 the hooks from the default location (/.../python-github-webhooks/hooks)
:telegram_token: Your bot's token. You can request a telegram API token from @BotFather
:server_url: The url of the server. This is used for generating preview links
:notify_branches: Pushes to those branches are send to telegram

Adding Hooks
============

This application will execute scripts in the hooks directory using the
following order:

::

    hooks/{event}-{name}-{branch}
    hooks/{event}-{name}
    hooks/{event}
    hooks/all

The application will pass to the hooks the path to a JSON file holding the
payload for the request as first argument. The event type will be passed
as second argument. For example:

::

    hooks/push-myrepo-master /tmp/sXFHji push

Hooks can be written in any scripting language as long as the file is
executable and has a shebang. A simple example in Python could be:

::

    #!/usr/bin/env python
    # Python Example for Python GitHub Webhooks
    # File: push-myrepo-master

    import sys
    import json

    with open(sys.argv[1], 'r') as jsf:
      payload = json.loads(jsf.read())

    ### Do something with the payload
    name = payload['repository']['name']
    outfile = '/tmp/hook-{}.log'.format(name)

    with open(outfile, 'w') as f:
        f.write(json.dumps(payload))

Not all events have an associated branch, so a branch-specific hook cannot
fire for such events. For events that contain a pull_request object, the
base branch (target for the pull request) is used, not the head branch.

Deploy
======

Apache
------

To deploy in Apache, just add a ``WSGIScriptAlias`` directive to your
VirtualHost file:

::

    <VirtualHost *:80>
        ServerAdmin you@my.site.com
        ServerName  my.site.com
        DocumentRoot /var/www/site.com/my/htdocs/

        # Handle Github webhook
        <Directory "/var/www/site.com/my/python-github-webhooks">
            Order deny,allow
            Allow from all
        </Directory>
        WSGIScriptAlias /webhooks /var/www/site.com/my/python-github-webhooks/webhooks.py

    </VirtualHost>

You can now add that URL to your Github repository settings:

    https://github.com/youruser/myrepo/settings/hooks

And add a Webhook to the WSGI script URL:

::

   http://my.site.com/webhooks

Docker
------

To deploy in a Docker container you have to expose the port 5000, for example
with the following command:

::
    
    git clone http://github.com/carlos-jenkins/python-github-webhooks.git
    docker build -t carlos-jenkins/python-github-webhooks python-github-webhooks
    docker run -d --name webhooks -p 5000:5000 carlos-jenkins/python-github-webhooks

You can also mount volume to setup the ``hooks/`` directory, and the file
``config.json``:

::

    docker run -d --name webhooks \
      -v /path/to/my/hooks:/src/hooks \
      -v /path/to/my/config.json:/src/config.json \
      -p 5000:5000 python-github-webhooks

Debug
=====

When running in Apache, the ``stderr`` of the hooks that return non-zero will
be logged in Apache's error logs. For example:

::

    sudo tail -f /var/log/apache2/error.log

Will log errors in your scripts if printed to ``stderr``.

You can also launch the Flask web server in debug mode at port ``5000``.

::

    python webhooks.py

This can help debug problem with the WSGI application itself.


License
=======

::

   Nextcloud - passman
   Copyright (c) 2016, Sander Brand (brantje@gmail.com)

   license GNU AGPL version 3 or any later version

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.


