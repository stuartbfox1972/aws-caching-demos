from app.connections import _rds_connect, _elasticache_connect
from app.elasticache import _elasticache_flush
from datetime import datetime
from flask import Response, request
from hurry.filesize import size

import hashlib
import json
import os
import pickle
import sys
import time

KEYSPACE=0

def _rds_query():
    r = _elasticache_connect(KEYSPACE)
    content = request.get_json(silent=True)
    key = 'RDS:' + content['Query']
    query = content['Query']
    hex_dig = hashlib.sha256(key.encode('utf-8')).hexdigest()

    if r.exists(hex_dig):
        start = datetime.now()
        data = pickle.loads(r.get(hex_dig))
        stop = datetime.now()
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE HIT",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload Size": size(sys.getsizeof(data))},
                              indent=1)
    else:
        db = _rds_connect()
        cursor = db.cursor()
        start = datetime.now()
        print("Running " + query + " at " + str(start))
        cursor.execute(query)
        data = cursor.fetchall()
        p_data = pickle.dumps(data)
        r.set(hex_dig, p_data, ex=900)
        stop = datetime.now()
        print("Finished " + query + " at " + str(stop))
        diff = (stop-start).total_seconds()
        payload = json.dumps({"Response": "CACHE MISS",
                              "Duration": str(diff),
                              "Measurement": "Seconds",
                              "Payload Size": size(sys.getsizeof(p_data))},
                              indent=1)

    return payload

    
def _rds_compare():
    ## Flush cache
    _elasticache_flush(KEYSPACE)
    ## Run initial query and populate cache
    q1_res = json.loads(_rds_query())
    q1_time = float(q1_res['Duration'])
    ## Run query from cache
    q2_res = json.loads(_rds_query())
    q2_time = float(q2_res['Duration'])
    ## Run query from cache
    q3_res = json.loads(_rds_query())
    q3_time = float(q3_res['Duration'])
    ## Run query from cache
    q4_res = json.loads(_rds_query())
    q4_time = float(q4_res['Duration'])
    ## Run query from cache
    q5_res = json.loads(_rds_query())
    q5_time = float(q5_res['Duration'])
    ## Run query from cache
    q6_res = json.loads(_rds_query())
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
    return payload

def _rds_flush():
    start = datetime.now()
    _elasticache_flush(KEYSPACE)
    stop = datetime.now()
    diff = (stop-start).total_seconds()

    payload = json.dumps({"Response": "Keys successfully deleted from Elasticache",
                          "Keyspace": KEYSPACE,
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=1)
    return payload