import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from service import status
from werkzeug.exceptions import NotFound

from flask_sqlalchemy import SQLAlchemy
from service.models.Vendor import Vendor, DataValidationError
from service.models.Product import Product
from service import app
from .Vendor import *
from .Product import *

@app.route("/")
def index():
    return (
        jsonify(
            name="REST API Service",
            version="1.0",
            paths=url_for("list_vendors", _external=True),
        ),
        status.HTTP_200_OK,
    )

def init_db():
    global app
    Vendor.init_db(app)
    Product.init_db(app)
