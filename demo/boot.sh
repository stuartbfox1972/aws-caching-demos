#!/bin/sh

HOME="/src"

cd ${HOME}
python -u populate_mysql.py &
python -u populate_dynamo.py &

/usr/bin/xray --bind=0.0.0.0:2000 --bind-tcp=0.0.0.0:2000 &

# Start flask listening on all interfaces
exec flask run --host=0.0.0.0 
