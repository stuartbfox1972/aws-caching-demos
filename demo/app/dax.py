from app.connections import *

import amazondax
import botocore.session
import json

def _dax_query():
    #region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    #endpoint_url, endpoint_port = os.environ.get('DAX_HOST').split(':')
    #print(endpoint_url)
    #table_name = os.environ.get('DYNAMODB_TABLE')
    #session = botocore.session.get_session()
    #dynamo_client = session.create_client('dynamodb', region_name=region)
    #dax_client = amazondax.AmazonDaxClient(session, region_name=region, endpoints=endpoint_url)

    #payload = json.dumps({"Response": "DAX"}, indent=1)
    return "DAX"