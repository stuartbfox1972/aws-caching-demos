import boto3
import os
import random
import string

for k, v in os.environ.items():
    print(f'{k}={v}')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

print('Checking DynamoDB')
try:
    response = table.get_item(
        Key={
            'serialNumber': 10001
        }
    )
    print(response['Item'])
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
