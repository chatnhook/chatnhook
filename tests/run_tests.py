from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import os
import json
from pprint import pprint
import requests
from time import sleep


def get_data_files(service):
    test_files = []
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_files = current_path + '/fixtures/' + service
    json_files = []
    for path, dirs, files in os.walk(data_files):
        for f in files:
            if '.json' in f:
                json_files.append(path+'/'+f)

    for js in json_files:
        # pprint(js)
        hook_name = js.replace('.json', '').split('-')[0].split('/')[-2:][0]
        print(hook_name)
        with open(os.path.join(data_files, js)) as json_file:
            content = json.load(json_file)
            test_files.append({
                'name': js,
                'event': hook_name,
                'post_data': content
            })

    return test_files


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
        print("Testing " + test_file['name'])
        try:
            result = send_request('http://localhost:5000/github', test_file['event'], test_file['post_data'])
            if result.status_code == 200:
                print("Success! \n")
            else:
                print("FAIL!")

        except requests.exceptions.ConnectionError:
            print("FAIL!")
        sleep(0.5)


if __name__ == '__main__':
    test_github()
