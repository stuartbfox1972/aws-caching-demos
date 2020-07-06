#!/usr/bin/env python

from decimal import *

import boto3
import datetime
import json
import multiprocessing
import os
import random
import string
import time

NORTHERNMOST = 49.
SOUTHERNMOST = 25.
EASTERNMOST  = -66.
WESTERNMOST  = -124.
SENSORS      = 500
RECORDS      = 10000
T            = SENSORS*RECORDS

# For testing against local
if 'DYNAMODB_ENDPOINT' in os.environ:
    store = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
    SENSORS = SENSORS/100
    RECORDS = RECORDS/100
else:
    store = boto3.resource('dynamodb')

sensorLocation = store.Table(os.environ['SENSORLOCATION_TABLE'])
sensorData = store.Table(os.environ['SENSORDATA_TABLE'])

item = sensorLocation.get_item(
  Key={
    'sensorName': 'sensor' + str(SENSORS-1)
  }
)

def _gen_lat_lng():
    lat = round(random.uniform(SOUTHERNMOST, NORTHERNMOST), 6)
    lng = round(random.uniform(EASTERNMOST, WESTERNMOST), 6)
    return(lat,lng)


def populate(start, end, stamps):
    for i in range(start, end):
        sensor = 'sensor' + str(i)
        sTime = startTime
        print(sensor)
        lat,lon = _gen_lat_lng()
        sensorLocation.put_item(
            Item={
                'sensorName': sensor,
                'lat': str(lat),
                'long': str(lon)
            }
        )
        with sensorData.batch_writer() as batchData:
            for stamp in stamps:
                item = {'sensorName': sensor, 'timestamp': stamp, 'datapoint': random.randint(20,90)}
                batchData.put_item(Item=item)

def start_workers(stamps):
    jobs = []
    for number in range(0, 500, 50):
        args = {"start":number,"end":(number+49), "stamps":stamps}
        p = multiprocessing.Process(target=populate, kwargs=args)
        jobs.append(p)
        p.start()



print('Checking DynamoDB')
if 'Item' not in item:
    print('Populating DynamoDB Table with ' + str(T), ' records, this could take a while')

    dt = datetime.datetime(2016, 2, 25, 23, 23)
    startTime=(round(time.mktime(dt.timetuple())))
    stamps = [startTime]
    for record in range(0, RECORDS):
        startTime += 10
        stamps.append(startTime)

    start_workers(stamps)

else:
    print("DynamoDB Table Already Populated with test data")