import os, json
from pprint import pprint
import requests
from time import sleep

def get_data_files(service):
    files = []
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_files = current_path + '/data/' + service
    json_files = [pos_json for pos_json in os.listdir(data_files) if pos_json.endswith('.json')]
    for js in json_files:
        # pprint(js)
        hook_name = js.replace('.json', '').split('-')[0]
        pprint(hook_name)
        with open(os.path.join(data_files, js)) as json_file:
            content = json.load(json_file)
            files.append({
                'name': js,
                'event': hook_name,
                'post_data': content
            })

    return files


def send_request(url, event, data=None):
    headers = {
        'content-type': 'application/json',
        'X-GitHub-Event': event
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r


def test_github():
    test_files = get_data_files('github')
    for test_file in test_files:
        print "Testing " + test_file['name']
        result = send_request('http://localhost:5000', test_file['event'], test_file['post_data'])
        if result.status_code == 200:
            print "Success! \n"
        else:
            print "FAIL!"
        sleep(2)


if __name__ == '__main__':
    test_github()
