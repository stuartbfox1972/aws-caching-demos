#!/bin/sh

HOME="/src"
MSTR="mysql -h ${DB_HOST} -u ${DB_USER} -p${DB_PASS} employees"

if ! ${MSTR} -e 'select count(1) from titles' &>/dev/null ; then
  cd /tmp
  git clone https://github.com/datacharmer/test_db
  cd test_db
  ${MSTR} < employees.sql
  cd /tmp
  rm -rf /tmp/test_db
else        
  cd ${HOME}
  exec flask run
fi
