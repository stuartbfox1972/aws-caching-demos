from flask import render_template, Response
from app import app

import os
import redis

def __init__():
    r = redis_connect()
    return r


@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1.0/elasticache/flush')
def elasticache_flush():
    r = redis_connect()
    r.flushall()
    return Response("{'Elasticache successfully flushed'}", mimetype='application/json')


@app.route('/api/v1.0/dax')
def dax():
    return Response("DAX", mimetype='application/json')


def redis_connect():
    r = redis.Redis(host=os.environ['CACHE_HOST'],
                    port=6379,
                    db=0)
    return r