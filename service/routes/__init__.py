'''
STARTING POINT FOR ROUTES
'''
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from service import status
from service.models import DataValidationError
from service.models.supplier_model import Supplier
from service.models.product_model import Product
from service import app
from .supplier_service import *
from .product_service import *

@app.route("/")
def index():
    ''' main index route '''
    return (
        jsonify(
            name="REST API Service",
            version="1.0",
            paths=url_for("list_suppliers", _external=True),
        ),
        status.HTTP_200_OK,
    )

def init_db(flask_app):
    ''' init db function '''
    Supplier.init_db(flask_app)
    Product.init_db(flask_app)
