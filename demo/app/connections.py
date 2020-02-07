from flask import Response

import json
import mysql.connector as mysql
import os
import redis

def redis_connect():
    try:
        r = redis.Redis(host=os.environ['CACHE_HOST'],
                        port=6379,
                        db=0)
        return r
    except redis.RedisError:
        payload=json.dumps({"Response": "Error Connecting to " + os.environ['CACHE_HOST']}, indent=1)
        return Response(payload, mimetype='application/json')

            
def db_connect():
    try:
        db = mysql.connect(host      = os.environ['DB_HOST'],
                            user     = os.environ['DB_USER'],
                            passwd   = os.environ['DB_PASS'],
                            database = 'employees')

        return db
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(e))