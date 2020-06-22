#!/bin/sh

HOME="/src"

cd ${HOME}
python -u populate_mysql.py &
python -u populate_dynamo.py &

/usr/bin/xray --bind=0.0.0.0:2000 --bind-tcp=0.0.0.0:2000 &

# Start gunicorn listening on all interfaces
exec gunicorn --chdir app demo:app -w 4 --threads 8 -b 0.0.0.0:5000 -t 120
