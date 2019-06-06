#!/bin/bash
# 用来展示 flask_apscheduler api 功能的脚本

echo '1. access host: curl 127.0.0.1:5000'
curl 127.0.0.1:5000
echo -e '\n'

echo '2. get jobs without auth: curl 127.0.0.1:5000/jobs'
curl 127.0.0.1:5000/jobs
echo -e '\n'

echo '3. get scheduler without auth: curl -X GET 127.0.0.1:5000/scheduler'
curl -X GET 127.0.0.1:5000/scheduler
echo -e '\n'

echo '4. inspect scheduler:  curl -H "Authorization: basic V29rbzpMaXU=" -X GET 127.0.0.1:5000/scheduler'
curl -H 'Authorization: basic V29rbzpMaXU=' -X GET 127.0.0.1:5000/scheduler
echo -e '\n'

echo '5. show jobs: curl -H "Authorization: basic V29rbzpMaXU=" -X GET 127.0.0.1:5000/scheduler/jobs'
curl -H 'Authorization: basic V29rbzpMaXU=' -X GET 127.0.0.1:5000/scheduler/jobs
echo -e '\n'

echo '6. add a new job: {"id": "job2", "func": "__main__:now", "trigger": "interval", "seconds": 3}'
curl -H 'Authorization: basic V29rbzpMaXU=' -X POST 127.0.0.1:5000/scheduler/jobs \
  -d '{"id": "job2", "func": "__main__:now", "trigger": "interval", "seconds": 3}'
echo -e '\n'

echo '7. add "job2" again: {"id": "job2", "func": "__main__:now", "trigger": "interval", "seconds": 3}'
curl -H 'Authorization: basic V29rbzpMaXU=' -X POST 127.0.0.1:5000/scheduler/jobs \
  -d '{"id": "job2", "func": "__main__:now", "trigger": "interval", "seconds": 30}'
echo -e '\n'

echo '8. show jobs: curl -H "Authorization: basic V29rbzpMaXU=" -X GET 127.0.0.1:5000/scheduler/jobs'
curl -H 'Authorization: basic V29rbzpMaXU=' -X GET 127.0.0.1:5000/scheduler/jobs
echo -e '\n'

