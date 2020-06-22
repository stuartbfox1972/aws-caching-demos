#!/usr/bin/env python

import boto3
import botocore.session
import json
import mysql.connector as mysql
import os
import requests

from subprocess import Popen, PIPE

WORKDIR='/tmp/'

def get_files():
    os.chdir(WORKDIR)
    url='https://raw.githubusercontent.com/datacharmer/test_db/master/'
    files= ['employees.sql',
            'load_departments.dump',
            'load_employees.dump',
            'load_dept_emp.dump',
            'load_dept_manager.dump',
            'load_titles.dump',
            'load_salaries1.dump',
            'load_salaries2.dump',
            'load_salaries3.dump',
            'show_elapsed.sql']
    for sqlfile in files:
        print("Downloading " + url + sqlfile)
        getter = requests.get(url + sqlfile)
        open(WORKDIR + sqlfile, 'wb').write(getter.content)


def rm_files():
    print("Cleaning up downloaded files")
    os.system('rm -rf ' + WORKDIR + '*')


def get_secret():
    if 'DB_HOST' in os.environ:
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_host = os.environ['DB_HOST']
        db_name = os.environ['DB_DB']
    else:
        secret_path = os.environ["SECRETS_MANAGER_PATH"]
        region_name = os.environ["AWS_DEFAULT_REGION"]

        sm_session = boto3.session.Session()
        sm_client = sm_session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = sm_client.get_secret_value(
                SecretId=secret_path
            )
        except ClientError as e:
            print("Something went wrong with Secrets Manager: {}".format(e))
        else:
            secret = json.loads(get_secret_value_response['SecretString'])
            db_user = secret['username']
            db_pass = secret['password']
            db_host = secret['host']
            db_name = secret['dbname']     
    
    return (db_user, db_pass, db_host, db_name)


def check_if_popluated():
    dbuser, dbpass, dbhost, dbname = get_secret()
    print("Checking Aurora")
    db = mysql.connect( host     = dbhost,
                        user     = dbuser,
                        passwd   = dbpass,
                        database = dbname)

    cursor = db.cursor()
    try:
        cursor.execute('select count(1) from titles')
        print("Database already populated, exiting")
    except:
        print("Database is empty, populating")
        get_files()
        executeSqlScript(dbuser, dbpass, dbhost, dbname)
        rm_files()

def executeSqlScript(dbuser, dbpass, dbhost, dbname, ignoreErrors=False):
    sourceCmd = "SOURCE %s" % ('employees.sql',)
    cmdList = [ "mysql",
                "-h", dbhost,
                "-u", dbuser,
                "-p" + dbpass,
                "--database", dbname,
                "--unbuffered" ] 
    if ignoreErrors : 
        cmdList.append( "--force" )
    else:
        cmdList.extend( ["--execute", sourceCmd ] )

    print("Inserting downloaded data")
    process = Popen( cmdList 
                   , cwd=WORKDIR
                   , stdout=PIPE 
                   , stderr=(STDOUT if ignoreErrors else PIPE) 
                   , stdin=(PIPE if ignoreErrors else None) )
    stdOut, stdErr = process.communicate( sourceCmd if ignoreErrors else None )
    if stdErr is not None and len(stdErr) > 0 : 
        print("Something went wrong inserting the data")
    return stdOut

check_if_popluated()
