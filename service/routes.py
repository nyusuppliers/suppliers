"""
Supplier Service

Routes:
- GET /suppliers - Return the list of all suppliers
- POST /suppliers - Create a new supplier in the database
- GET /suppliers/{id} - Return the supplier with a given id number
- PUT /suppliers/{id} - Update a supplier record in the database
- DELETE /suppliers/{id} - Delete a supplier record in the database
- GET /suppliers/favorites - Return the list of all suppliers marked as favorites previously
- GET /suppliers/?search={text}&supplier-id={id}&category=${category}&supplier-name=${name}
    - Return the list of all suppliers according to the search query
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
            #path=url_for("list_suppliers", _external=True)
        ),
        status.HTTP_200_OK
    )

######################################################################
# LIST ALL SUPPLIERS
######################################################################
@app.route("/suppliers", methods=["GET"])
def list_suppliers():
    """Returns all of the Suppliers"""
    app.logger.info('Request to list Suppliers...')

    name = request.args.get('name')
    phone = request.args.get('phone')
    address = request.args.get('address')
    available = request.args.get('available')
    rating = request.args.get('rating')
    product_id = request.args.get('product_id')

    # "available": True,
    # "product_list": [1,2,4,5],
    # "rating": 3.5
    if name:
        app.logger.info('Find suppliers by name: %s', name)
        suppliers = Supplier.find_by_name(name)
    elif phone:
        app.logger.info('Find suppliers with phone number: %s', phone)
        suppliers = Supplier.find_by_phone(phone)
    elif address:
        app.logger.info('Find suppliers with address: %s', address)
        suppliers = Supplier.find_by_address(address)
    elif available:
        app.logger.info('Find all suppliers that are available: %s', available)
        suppliers = Supplier.find_by_availability(available)
    elif rating:
        app.logger.info('Find suppliers with rating greater than: %s', rating)
        rating = float(rating)
        suppliers = Supplier.find_by_greater_rating(rating)
    elif product_id:
        app.logger.info('Find suppliers containing product with id %s in their products', \
            product_id)
        product_id = int(product_id)
        suppliers = Supplier.find_by_product(product_id)
    else:
        app.logger.info('Find all suppliers')
        suppliers = Supplier.all()

    results = [supplier.serialize() for supplier in suppliers]
    app.logger.info("Returning %d suppliers", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A SUPPLIER (READ)
######################################################################
@app.route("/suppliers/<int:supplier_id>", methods=["GET"])
def get_suppliers(supplier_id):
    """
    Retrieve a single Supplier

    This endpoint will return a Supplier based on it's id
    """
    app.logger.info("Request for supplier with id: %s", supplier_id)
    supplier = Supplier.find(supplier_id)
    if not supplier:
        raise NotFound("Supplier with id '{}' was not found.".format(supplier_id))

    app.logger.info("Returning supplier: %s", supplier.name)
    return make_response(jsonify(supplier.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW SUPPLIER
######################################################################
@app.route("/suppliers", methods=["POST"])
def create_suppliers():
    """
    ADD A NEW SUPPLIER
    """
    app.logger.info("Create a new supplier")
    check_content_type("application/json")
    supplier = Supplier()
    supplier.deserialize(request.get_json())
    supplier.create()
    message = supplier.serialize()
    location_url = url_for("get_suppliers", supplier_id=supplier.id, _external=True)

    app.logger.info("Supplier with ID [%s] created.", supplier.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# UPDATE AN EXISTING SUPPLIER
######################################################################
@app.route("/suppliers/<int:supplier_id>", methods=["PUT"])
def update_suppliers(supplier_id):
    """
    Update a Supplier

    This endpoint will update a Supplier based the body that is posted
    """
    app.logger.info("Request to update supplier with id: %s", supplier_id)
    check_content_type("application/json")
    supplier = Supplier.find(supplier_id)
    if not supplier:
        raise NotFound("Supplier with id '{}' was not found.".format(supplier_id))
    supplier.deserialize(request.get_json())
    supplier.id = supplier_id
    supplier.update()

    app.logger.info("Supplier with ID [%s] updated.", supplier.id)
    return make_response(jsonify(supplier.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A SUPPLIER
######################################################################
@app.route("/suppliers/<int:supplier_id>", methods=["DELETE"])
def delete_suppliers(supplier_id):
    """
    Delete a Supplier

    This endpoint will delete a Supplier based the id specified in the path
    """
    app.logger.info("Request to delete supplier with id: %s", supplier_id)
    supplier = Supplier.find(supplier_id)
    if supplier:
        supplier.delete()

    # app.logger.info("Supplier with ID [%s] delete complete.", supplier_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# PATH: /suppliers/{supplier_id}/penalize
######################################################################
@app.route("/suppliers/<supplier_id>/penalize", methods=["PUT"])
def penalize(supplier_id):
    """
    Penalize a supplier
    """
    app.logger.info("Request to penalize supplier with id: %s", supplier_id)
    check_content_type("application/json")
    supplier = Supplier.find(supplier_id)
    if not supplier:
        raise NotFound("supplier with id '{}' was not found.".format(supplier_id))
    if supplier.rating >= 1:
        supplier.rating -= 1
    else:
        supplier.rating = 0
    supplier.update()

    app.logger.info("Customer with ID [%s] penalized.", supplier.id)
    return make_response(jsonify(supplier.serialize()), status.HTTP_200_OK)

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
        "Content-Type must be {}".format(media_type),)
