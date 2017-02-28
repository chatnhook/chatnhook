
# Captain Hook

A web server to receive webhooks from many online services and forward the information
to many different messaging platforms, like Telegram or Slack, using a different
template for each.

A **service** represents any web service that sends a webhook.

An **event** is identified from the given webhook (like a push on Github, for example)

A **comm** is then used to publish information from this hook in messaging services.

## Dependencies

- Python 3.6

`sudo pip install -r requirements.txt`


## Running

`hug -f captain_hook/endpoint.py`

## Currently supported services and events

- Github
- Docker
- Pagerduty
- Patreon
- Scrutinizer
- Slack
- Travis

## Currently supported comms to publish event information

- Telegram
- Slack
- Discord
- Mattermost

## Adding your own service

To add your own service you need to follow a few simple steps. Let's say, for example,
you want to process hooks from a service called `Foobar`.

1. Create a `foobar` folder inside the `services` folder;
2. Inside it, create a file named `foobar.py` with the following contents:

```python
from ..base import BaseService


class FoobarService(BaseService):

    @property
    def event(self):
        return self.request.headers['X-GITHUB-EVENT']

```

3. Modify the `event` property as necessary to identify the the event sent by
   the service. Later you're gonna create a script to handle this event. Inside
   this class you have access to `self.request` and `self.body` to do whatever
   you want.
4. Still in the `foobar` folder, create a `__init__.py` with the following contents:

`from .foobar import FoobarService`

5. Now it's time to create the event processor. Inside the `foobar` folder, create
   a folder named `events`, and inside it create a script with the name of an
   event that will be identified by the `event` property of the service class.
   For instance, let's say the service only sends one event: `bark`. So you create
   `bark.py` with these contents:

```python
from ...base.events import BaseEvent


class BarkEvent(BaseEvent):

    def process(self):
        return {'default': str(self.event)}

```

6. Modify the `process` method as desired. In the event class you have access
   to the variables `self.event`, `self.body` and `self.request`. You need to return
   a dict with **comm** names as keys, like `telegram`, and the values are the messages
   each **comm** will publish for that event. If you want the same message for all **comms**
   that do not have a specific one, use the `default` key.

7. Finally, in `endpoint.py` you import your service and add it to the service
dictionary, like this:

```python
from services.foobar import FoobarService

SERVICES = {
    "foobar": FoobarService
}
```

NOTE: service discovery is going to become automatic and there will be a settings
file to enable them soon.

## Adding your comms

**Work in progress.**
