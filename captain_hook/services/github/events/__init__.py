from ...base.events import BaseEvent
import requests
from json import loads


class GithubEvent(BaseEvent):
	def gh_api(self, url):
		if 'https://api.github.com/' not in url:
			url = 'https://api.github.com/' + url

		headers = {
			'User-Agent': 'Hookbot',
		}
		if 'token' in self.config:
			headers['Authorization'] = 'token ' + self.config.get('token')

		response = requests.get(url=url, headers=headers)

		try:
			result = loads(response.text)
		except TypeError:
			result = False

		return result
