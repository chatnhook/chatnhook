import hug
import utils
from adapters.github import GithubAdapter

SERVICE_ADAPTERS = {
    "github": GithubAdapter
}

@hug.get('/{service}')
@hug.post('/{service}')
def receive_webhook(request, body, service: hug.types.text):
    return SERVICE_ADAPTERS[service](request, body).execute()
