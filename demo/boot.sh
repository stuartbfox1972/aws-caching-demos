#!/bin/sh

HOME="/src"
MSTR="mysql -h ${DB_HOST} -u ${DB_USER} -p${DB_PASS} ${DB_DB}"

# Test if the required database and tables exist, if not, create them
if ! ${MSTR} -e 'select count(1) from titles' &>/dev/null ; then
  echo "INSERTING MYSQL DATA"
  cd /tmp
  git clone https://github.com/datacharmer/test_db
  cd test_db
  ${MSTR} < employees.sql
  rm -rf /tmp/test_db
else
  echo "MYSQL DATA ALREADY INSERTED"
fi

python -u check_dynamo.py

cd ${HOME}
# Start flask listening on all interfaces
exec flask run --host=0.0.0.0 
