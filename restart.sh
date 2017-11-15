#!/bin/bash
kill $(ps aux | grep 'endpoint.py' | awk '{print $2}')
pip install -r requirements.txt
/etc/init.d/hook-bot restart