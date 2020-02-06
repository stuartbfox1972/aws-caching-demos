from app import app
from datetime import datetime
from flask import render_template, Response, request
from hurry.filesize import size

import amazondax
import botocore.session
import hashlib
import json
import mysql.connector as mysql
import os
import pickle
import redis
import sys
import time


@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1.0/elasticache/flush', methods=['GET'])
def elasticache_flush():
    payload = _elasticache_flush()
    return Response(payload,
                    mimetype='application/json')


def _elasticache_flush():
    r = redis_connect()
    start = datetime.now()
    r.flushall()
    stop = datetime.now()
    diff = (stop-start).total_seconds()
    payload = json.dumps({"Response": "Elasticache successfully flushed",
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload


@app.route('/api/v1.0/elasticache/query', methods=['POST'])
def elasticache_query():
    payload = _elasticache_query()
    return Response(payload,
                    mimetype='application/json')


def _elasticache_query():
    r = redis_connect()
    content = request.get_json(silent=True)
    key = os.environ['DB_DB'] + ':' + content['Query']
    query = content['Query']
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
        return payload
    else:
        try:
            db = db_connect()
            cursor = db.cursor()
            start = datetime.now()
            #cursor.execute('RESET QUERY CACHE')
            cursor.execute(query)
            data = cursor.fetchall()
            p_data = pickle.dumps(data)
            r.set(hex_dig, p_data)
            stop = datetime.now()
            diff = (stop-start).total_seconds()
            payload = json.dumps({"Response": "CACHE MISS",
                                  "Duration": str(diff),
                                  "Measurement": "Seconds",
                                  "Payload Size": size(sys.getsizeof(p_data))},
                                  indent=1)
            return payload
        except mysql.connector.Error as e:
            payload = json.dumps({"Response": "Something went wrong: {}".format(e)},
                                  indent=1)
            return payload


@app.route('/api/v1.0/elasticache/compare', methods=['POST'])
def elasticache_compare():

    ## Flush cache
    _elasticache_flush()
    ## Run initial query and populate cache
    q1_res = json.loads(_elasticache_query())
    q1_time = float(q1_res['Duration'])
    ## Run query from cache
    q2_res = json.loads(_elasticache_query())
    q2_time = float(q2_res['Duration'])
    ## Run query from cache
    q3_res = json.loads(_elasticache_query())
    q3_time = float(q3_res['Duration'])
    ## Run query from cache
    q4_res = json.loads(_elasticache_query())
    q4_time = float(q4_res['Duration'])
    ## Run query from cache
    q5_res = json.loads(_elasticache_query())
    q5_time = float(q5_res['Duration'])
    ## Run query from cache
    q6_res = json.loads(_elasticache_query())
    q6_time = float(q6_res['Duration'])

    avg_time =  (q2_time + q3_time + q4_time + q5_time + q6_time) / 5

    diff = ("%.2f" % ((q1_time/avg_time)*100) )
    miss = ("%.4f" % float(q1_res['Duration']))
    hit = ("%.4f" % float(avg_time))

    payload = json.dumps({"MISS Query Time": miss,
                          "AVG HIT Query Time": hit,
                          "Measurement": "Seconds",
                          "Payload Size": q1_res['Payload Size'],
                          "Percentage Increase": str(diff) +"%"
                        }, indent=1)

    return Response(payload,
                    mimetype='application/json')

@app.route('/api/v1.0/dax/query')
def dax():
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    endpoint_url, endpoint_port = os.environ.get('DAX_HOST').split(':')
    print(endpoint_url)
    table_name = os.environ.get('DYNAMODB_TABLE')
    session = botocore.session.get_session()
    dynamo_client = session.create_client('dynamodb', region_name=region)
    dax_client = amazondax.AmazonDaxClient(session, region_name=region, endpoints=endpoint_url)

    payload = json.dumps({"Response": "DAX"}, indent=1)
    return Response(payload, mimetype='application/json')


def redis_connect():
    try:
        r = redis.Redis(host=os.environ['CACHE_HOST'],
                        port=6379,
                        db=0)
        return r
    except redis.RedisError as e:
        payload=json.dumps({"Response": "Error Connecting to " + os.environ['CACHE_HOST']}, indent=1)
        return Response(payload, mimetype='application/json')

            
def db_connect():
    try:
        db = mysql.connect(host      = os.environ['DB_HOST'],
                            user     = os.environ['DB_USER'],
                            passwd   = os.environ['DB_PASS'],
                            database = 'employees')

        return db
    except mysql.connector.Error as e:
        print("Something went wrong: {}".format(err))
