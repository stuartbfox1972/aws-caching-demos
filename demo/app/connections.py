from flask import Response

import boto3
import json
import mysql.connector as mysql
import os
import redis

def _elasticache_connect():
    try:
        r = redis.Redis(host=os.environ['CACHE_HOST'],
                        port=6379,
                        db=0)
        return r
    except redis.RedisError:
        payload=json.dumps({"Response": "Error Connecting to " + os.environ['CACHE_HOST']}, indent=1)
        return Response(payload, mimetype='application/json')

            
def _rds_connect():
    try:
        db = mysql.connect(host      = os.environ['DB_HOST'],
                            user     = os.environ['DB_USER'],
                            passwd   = os.environ['DB_PASS'],
                            database = 'employees')

        return db
    except mysql.Error as e:
        print("Something went wrong: {}".format(e))


def _dax_connect():
    return


def _dynamodb_connect():
    return


def _s3_connect():
    if 'S3_ENDPOINT' in os.environ:
        s3 = boto3.resource('s3', endpoint_url=os.environ['S3_ENDPOINT'])
    else:
        s3 = boto3.resource('s3')

    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    return (s3, bucket)