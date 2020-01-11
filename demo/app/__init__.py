import boto3
from flask import Flask
from flask_bootstrap import Bootstrap
import os
import random
import string

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

try:
    response = table.get_item(
        Key={
            'serialNumber': 9999
        }
    )
    print('DynamoDB Table Already Populated')
except:
    print('Populating DynamoDB Table')
    batchsize=1000
    for i in range(0, 10000, batchsize):
        print(i)
        with table.batch_writer() as batch:
            for item in range(i, i+batchsize):
                res = ''.join(random.choices(string.ascii_uppercase + 
                    string.digits, k = 500))
                batch.put_item(
                    Item={
                        'serialNumber': item,
                        'text': res
                    }
                )

app = Flask(__name__)

from app import routes

bootstrap = Bootstrap(app)
