from amazondax import AmazonDaxClient
from flask import Response
from rediscluster import RedisCluster

import boto3
import botocore.session
import json
import mysql.connector as mysql
import os


def get_secret():

    if 'DB_HOST' in os.environ:
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_host = os.environ['DB_HOST']
        db_name = 'employees'
    else:
        secret_path = os.environ["SECRETS_MANAGER_PATH"]
        region_name = os.environ["REGION"]

        # Create a Secrets Manager client
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
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            secret = json.loads(get_secret_value_response['SecretString'])
            db_user = secret['username']
            db_pass = secret['password']
            db_host = secret['host']
            db_name = secret['dbname']     
        return (db_user, db_pass, db_host, db_name)


def _elasticache_connect():
    try:
        startup_nodes = [{"host": os.environ['CACHE_HOST'],
                          "port": "6379"}]
        r = RedisCluster(decode_responses=True,
                         startup_nodes=startup_nodes,
                         skip_full_coverage_check=True)
        return r
    except redis.RedisError:
        payload=json.dumps({"Response": "Error Connecting to " + os.environ['CACHE_HOST']}, indent=1)
        return Response(payload, mimetype='application/json')

            
def _rds_connect():
    try:
        dbuser, dbpass, dbhost, dbname = get_secret()
        db = mysql.connect(host     = dbhost,
                           user     = dbuser,
                           passwd   = dbpass,
                           database = dbname)

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