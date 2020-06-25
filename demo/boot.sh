#!/bin/sh

HOME="/src"

cd ${HOME}
python -u populate_mysql.py &
python -u populate_dynamo.py &

/usr/bin/xray --bind=0.0.0.0:2000 --bind-tcp=0.0.0.0:2000 &

# Start gunicorn listening on all interfaces
exec gunicorn --chdir app demo:app \
              --workers 4 \
              --threads 8 \
              --access-logfile - \
              --error-logfile - \
              --timeout 300 \
              --bind 0.0.0.0:5000
