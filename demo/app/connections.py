from amazondax import AmazonDaxClient
from flask import Response

import boto3
import botocore.session
import json
import mysql.connector as mysql
import os
import redis

def _elasticache_connect(db):
    try:
        r = redis.Redis(host=os.environ['CACHE_HOST'],
                        port=6379,
                        db=db)
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


def _dynamodb_connect():
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    if 'DYNAMODB_ENDPOINT' in os.environ:
        dynamo_client = boto3.resource('dynamodb',
                                  region_name=region,
                                  endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
        dax_client = boto3.resource('dynamodb',
                                  region_name=region,
                                  endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
    else:
        endpoint_url, endpoint_port = os.environ.get('DAX_HOST').split(':')
        dynamo_client = boto3.resource('dynamodb',
                                        region_name=region)
        dax_client = AmazonDaxClient.resource(region_name=region,
                                              endpoint_url=endpoint_url)
    
    return (dynamo_client, dax_client)


def _s3_connect():
    if 'S3_ENDPOINT' in os.environ:
        s3 = boto3.resource('s3', endpoint_url=os.environ['S3_ENDPOINT'])
    else:
        s3 = boto3.resource('s3')

    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    return (s3, bucket)