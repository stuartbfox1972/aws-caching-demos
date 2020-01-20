from app import app
from datetime import datetime
from flask import render_template, Response, request
from hurry.filesize import size

import hashlib
import json
import mysql.connector as mysql
import os
import pickle
import redis
import sys


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
    r = redis_connect()
    start = datetime.now()
    r.flushall()
    stop = datetime.now()
    diff = (stop-start).total_seconds()
    payload = json.dumps({"Response": "Elasticache successfully flushed",
                          "Duration": str(diff) + " seconds"}, indent=1)
    return Response(payload,
                    mimetype='application/json')


@app.route('/api/v1.0/elasticache/query', methods=['POST'])
def elasticache_query():
    r = redis_connect()
    content = request.get_json(silent=True)
    q = content['Query'].encode('utf-8')
    hex_dig = hashlib.sha256(q).hexdigest()

    if r.exists(hex_dig):
        start = datetime.now()
        data = r.get(hex_dig)
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE HIT",
                          "Duration": str(diff) + " seconds",
                          "Payload Size": size(sys.getsizeof(data))})
        return Response(payload, mimetype='application/json')
    else:
        try:
            db = db_connect()
            cursor = db.cursor()
            start = datetime.now()
            cursor.execute(q)
            data = cursor.fetchall()
            p_data = pickle.dumps(data)
            r.set(hex_dig, p_data)
            stop = datetime.now()
            diff = (stop-start).total_seconds()
            payload = json.dumps({"Response": "CACHE MISS",
                                "Duration": str(diff) + " seconds",
                                "Payload Size": size(sys.getsizeof(p_data))})
            return Response(payload, mimetype='application/json')
        except mysql.connector.Error as e:
            payload = json.dumps({"Response": "Something went wrong: {}".format(e)})
            return Response(payload, mimetype='application/json')

@app.route('/api/v1.0/dax')
def dax():
    payload = json.dumps({"Response": "DAX"})
    return Response(payload, mimetype='application/json')


def redis_connect():
    try:
        r = redis.Redis(host=os.environ['CACHE_HOST'],
                        port=6379,
                        db=0)
        return r
    except redis.RedisError as e:
        print(e)
        payload=json.dumps({"Response": "Error Connecting to os.environ['CACHE_HOST']"})
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