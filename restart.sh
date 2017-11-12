#!/bin/bash
kill $(ps aux | grep 'endpoint.py' | awk '{print $2}')
/etc/init.d/hook-bot restart