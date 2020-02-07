from app import app
#from app.elasticache import *
from app.elasticache import _elasticache_compare, _elasticache_flush, _elasticache_query
from app.dax import *
from app.s3 import *
from flask import render_template, Response


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
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/elasticache/query', methods=['POST'])
def elasticache_query():
    payload = _elasticache_query()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/elasticache/compare', methods=['POST'])
def elasticache_compare():
    payload = _elasticache_compare()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/dax/query')
def dax():
    payload = _dax_query()
    return Response(payload, mimetype='application/json')
