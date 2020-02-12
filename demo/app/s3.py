from app.connections import _elasticache_connect, _s3_connect
from datetime import datetime
from hurry.filesize import size

import hashlib
import json
import os
import pickle
import random
import string
import sys

BATCH=10

def _s3_prepare():
    s3, bucket = _s3_connect()
    start = datetime.now()
    for i in range(0, BATCH):
        data = ''.join(random.choices(string.ascii_uppercase + 
                    string.digits, k = 10240000))
        bucket.put_object(Key="dummy" + str(i),
                          Body=data)
    stop = datetime.now()
    diff = (stop-start).total_seconds()

    payload = json.dumps({"Response": "S3 data successfully created",
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload


def _s3_query():
    r = _elasticache_connect()
    s3, bucket = _s3_connect()
    f = random.randint(0, BATCH)
    key = 'S3:' + (os.environ['S3_BUCKET']) + ':' + 'dummy' + str(f)
    hex_dig = hashlib.sha256(key.encode('utf-8')).hexdigest()
    if r.exists(hex_dig):
        start = datetime.now()
        data = r.get(hex_dig)
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE HIT",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload Size": size(sys.getsizeof(data))},
                              indent=1)
    else:
        start = datetime.now()
        obj = s3.Object(os.environ['S3_BUCKET'], 'dummy1')
        data = obj.get()['Body'].read().decode('utf-8')
        p_data = pickle.dumps(data)
        r.set(hex_dig, p_data)
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE MISS",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload Size": size(sys.getsizeof(data))},
                              indent=1)
    
    return payload


def _s3_compare():
    return "Compare"

def _s3_clean():
    start = datetime.now()
    s3, bucket = _s3_connect()
    keys = bucket.objects.all()
    for obj in bucket.objects.all():
        bucket.Object(obj.key).delete()
        print(obj.key)

    stop = datetime.now()
    diff = (stop-start).total_seconds()

    payload = json.dumps({"Response": "S3 data successfully deleted",
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload