from app import app
from app.elasticache import _elasticache_flus
from app.rds import _rds_compare, _rds_query, _rds_flush
from app.s3 import _s3_prepare, _s3_clean, _s3_query, _s3_flush
from app.ddb import _ddb_query
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
    payload = _elasticache_flush()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/rds/query', methods=['POST'])
def rds_query():
    payload = _rds_query()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/rds/compare', methods=['POST'])
def rds_compare():
    payload = _rds_compare()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/s3/prepare')
def s3_prepare():
    payload = _s3_prepare()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/s3/clean')
def s3_clean():
    payload = _s3_clean()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/s3/query')
def s3_query():
    payload = _s3_query()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/s3/compare')
def s3_compare():
    payload = _s3_compare()
    return Response(payload, mimetype='application/json')


@app.route('/api/v1.0/ddb/query', methods=['POST'])
def ddb_query():
    payload = _ddb_query()
    return Response(payload, mimetype='application/json')