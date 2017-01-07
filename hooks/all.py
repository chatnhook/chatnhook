#!/usr/bin/env python
# Python Example for Python GitHub Webhooks
# File: push-myrepo-master

import sys
import json
from pprint import pprint
import logging
logging.basicConfig(level=logging.INFO)

with open(sys.argv[1], 'r') as jsf:
  payload = json.loads(jsf.read())

#pprint(payload)
### Do something with the payload
#name = payload['repository']['name']
#outfile = 'hook-{}.log'.format(name)

#with open(outfile, 'w') as f:
    #f.write(json.dumps(payload))