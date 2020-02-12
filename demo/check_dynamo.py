import boto3
import os
import random
import string

# For testing against local 
if 'DYNAMODB_ENDPOINT' in os.environ:
    dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
    print('LOCAL')
else:
    dynamodb = boto3.resource('dynamodb')
    print('REMOTE')

table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


item = table.get_item(
  Key={
    'serialNumber': 99999
  }
)

print('Checking DynamoDB')
if 'Item' not in item:
    print('Populating DynamoDB Table')
    batchsize=1000
    for i in range(0, 100000, batchsize):
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
else:
    print("DynamoDB Table Already Populated with test data")
