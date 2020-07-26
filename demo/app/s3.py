from app.connections import _elasticache_connect, _s3_connect
from app.elasticache import _elasticache_flush
from datetime import datetime
from hurry.filesize import size

import hashlib
import json
import os
import pickle
import random
import string
import sys

BATCH=500

def _s3_prepare():
    s3, bucket = _s3_connect()
    start = datetime.now()
    for i in range(0, BATCH):
        data = ''.join(random.choices(string.ascii_uppercase + 
                    string.digits, k = 5120000))
        bucket.put_object(Key="dummy" + str(i),
                          Body=data)
    stop = datetime.now()
    diff = (stop-start).total_seconds()

    payload = json.dumps({"Response": "S3 data successfully created",
                          "Objects Created": str(BATCH),
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload


def _s3_query():
    r = _elasticache_connect()
    s3, bucket = _s3_connect()
    f = random.randint(0, BATCH)
    fname = 'dummy' + str(f)
    key = 'S3:' + (os.environ['S3_BUCKET']) + ':' + fname
    hex_dig = hashlib.sha256(key.encode('utf-8')).hexdigest()
    if r.exists(hex_dig):
        start = datetime.now()
        data = pickle.loads(r.get(hex_dig))
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE HIT",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload": fname,
                              "Payload Size": size(sys.getsizeof(data))},
                              indent=1)
    else:
        start = datetime.now()
        obj = s3.Object(os.environ['S3_BUCKET'], fname)
        data = obj.get()['Body'].read().decode('utf-8')
        p_data = pickle.dumps(data)
        r.set(hex_dig, p_data, ex=900)
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE MISS",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload": fname,
                              "Payload Size": size(sys.getsizeof(data))},
                              indent=1)
    
    return payload


def _s3_compare():
    return "Compare"


def _s3_clean():
    counter = 0
    start = datetime.now()
    s3, bucket = _s3_connect()
    keys = bucket.objects.all()
    for obj in bucket.objects.all():
        counter += 1
        bucket.Object(obj.key).delete()

    stop = datetime.now()
    diff = (stop-start).total_seconds()

    payload = json.dumps({"Response": "S3 data successfully deleted",
                          "Objects Deleted": str(counter),
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload
