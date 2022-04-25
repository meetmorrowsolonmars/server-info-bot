#!/usr/bin/env bash

echo $$ >cron.pid

trap 'echo "Exit"; exit 0' SIGSTOP SIGINT

# set default timeout for cron
if [ -z "$1" ]; then
  #  timeout 30s by default
  TIMEOUT=30
else
  TIMEOUT=$1
fi

echo "Save server statistics every ${TIMEOUT}s"

export PYTHONPATH=$(pwd)

for (( ; ; )); do

  echo "[$(date)] Run save jobs"
  ./venv/bin/python ./src/cron/save_disk_space_statistics.py
  ./venv/bin/python ./src/cron/save_system_load_statistics.py
  sleep $TIMEOUT

done
