"""
Supplier Service

Routes:
- GET /suppliers - return the list of all suppliers 
- POST /suppliers - create a new supplier in the database 
- GET /suppliers/{id} - Returns the supplier with a given id number
- PUT /suppliers/{id} - updates a supplier record in the database
- DELETE /suppliers/{id} - deletes a supplier record in the database
- GET /suppliers/favorites - return the list of all suppliers marked as favorites previously
- GET /suppliers/?search={text}&supplier-id={id}&category=${category}&supplier-name=${name} - return the list of all suppliers according to the search query

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
from service.models import Supplier, DataValidationError, FavoriteSupplier

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
    app.logger.info("Request for suppliers list")
    suppliers = []
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
    supplier = Supplier.find_or_404(supplier_id)

    app.logger.info("Returning supplier: %s", supplier.name)
    return make_response(jsonify(supplier.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW SUPPLIER
######################################################################
@app.route("/suppliers", methods=["POST"])
def create_suppliers():
    app.logger.info("Create a new supplier")
    check_content_type("application/json")
    supplier = Supplier()
    supplier.deserialize(request.get_json())
    supplier.create()
    message = supplier.serialize()
    #location_url = url_for("get_supplier", supplier_id=supplier.id, _external=True)

    app.logger.info("Supplier with ID [%s] created.", supplier.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED
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
    # """
    # Delete a Supplier

    # This endpoint will delete a Supplier based the id specified in the path
    # """
    app.logger.info("Request to delete supplier with id: %s", supplier_id)
    supplier = Supplier.find(supplier_id)
    if supplier:
        supplier.delete()

    # app.logger.info("Supplier with ID [%s] delete complete.", supplier_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# LIST ALL FAVORITE SUPPLIERS
######################################################################
@app.route("/suppliers/favorites", methods=["GET"])
def list_favorite_suppliers():
    """Returns all of the Suppliers"""
    results = FavoriteSupplier.all()
    results = [r.Supplier.serialize() for r in results]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# ADD SUPLIER IN FAVORITE LIST
######################################################################
@app.route("/suppliers/favorites", methods=["POST"])
def create_favorite_suppliers():
    """ALL SUPPLIER IN FAVORITE LIST"""
    app.logger.info("Create a new supplier favorite")
    check_content_type("application/json")
    supplier = FavoriteSupplier()
    supplier.deserialize(request.get_json())
    supplier.create()
    message = supplier.serialize()
    #location_url = url_for("get_supplier", supplier_id=supplier.id, _external=True)

    app.logger.info("Supplier with ID [%s] created.", supplier.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED
    )


######################################################################
# QUERY SUPPLIERS
######################################################################
@app.route("/suppliers/?search={text}&supplier-id={id}&category=${category}&supplier-name=${name}", methods=["GET"])
def query_suppliers():
    # """Returns all of the Suppliers"""
    # app.logger.info("Request for pet list")
    # pets = []
    # category = request.args.get("category")
    # name = request.args.get("name")
    # if category:
    #     pets = Pet.find_by_category(category)
    # elif name:
    #     pets = Pet.find_by_name(name)
    # else:
    #     pets = Pet.all()

    # results = [pet.serialize() for pet in pets]
    # app.logger.info("Returning %d pets", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Supplier.init_db(app)
    FavoriteSupplier.init_db(app)

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