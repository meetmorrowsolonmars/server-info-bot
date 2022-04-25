# Server Info Bot

## Before running

Create a Python virtual environment. Install the required dependencies.
Perform a database migration.

```shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt

alembic upgrade head
```

## Run

Run a background process that will save server information every 45 seconds.

```shell
nohup ./cron.sh 45 &
```

Check logs.

```shell
cat ./nohup.out
```

Stop the background process.

```shell
./stop-cron.sh
```

If you want to use an alternative way to run scripts. Add to crontab

```shell
crontab -e

# TODO: commands for start
```
