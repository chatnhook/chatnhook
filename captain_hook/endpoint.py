import hug
import utils
from services.github import GithubService

SERVICES = {
    "github": GithubService
}

@hug.get('/{service}')
@hug.post('/{service}')
def receive_webhook(request, body, service: hug.types.text):
    return SERVICES[service](request, body).execute()
