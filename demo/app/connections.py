from amazondax import AmazonDaxClient
from flask import Response

import boto3
import botocore.session
import json
import mysql.connector as mysql
import os
import redis


def get_secret():

    if 'DB_USER' in os.environ:
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
    else:
        secret_path = os.environ["SECRET_MANAGER_PATH"]
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
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            secret = json.loads(get_secret_value_response['SecretString'])
            
            db_user = secret['username']
            db_pass = secret['password']
               
        return (db_user, db_pass)

print(get_secret())
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
        dbuser, dbpass = get_secret()
        db = mysql.connect(host      = os.environ['DB_HOST'],
                            user     = dbuser,
                            passwd   = dbpass,
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