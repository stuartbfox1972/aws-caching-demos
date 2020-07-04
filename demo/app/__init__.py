from flask import Flask
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

patch_all()

app = Flask(__name__)
from app import routes

xray_recorder.configure(service='CacheDemo')
XRayMiddleware(app, xray_recorder)

