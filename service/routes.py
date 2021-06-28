"""
Supplier Service

Routes:
- GET /suppliers - return the list of all suppliers 
- POST /suppliers - create a new supplier in the database 

"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Supplier, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="E-commerce Supplier REST API Service",
            version="1.0",
            path=url_for("list_suppliers", _external=True)
        ),
        status.HTTP_200_OK
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Supplier.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

######################################################################
# LIST ALL SUPPLIERS
######################################################################
@app.route("/suppliers", methods=["GET"])
def list_suppliers():
    app.logger.info("Request for all supplier list")
    suppliers = []
    suppliers = Supplier.all()

    results = [Supplier.serialize() for supplier in suppliers]
    app.logger.info("Returning %d suppliers", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# ADD A NEW PET
######################################################################
@app.route("/suppliers", methods=["POST"])
def create_pets():
    app.logger.info("Create a new supplier")
    check_content_type("application/json")
    supplier = Supplier()
    supplier.deserialize(request.get_json())
    supplier.create()
    message = supplier.serialize()
    location_url = url_for("get_supplier", supplier_id=supplier.id, _external=True)

    app.logger.info("Supplier with ID [%s] created.", supplier.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )