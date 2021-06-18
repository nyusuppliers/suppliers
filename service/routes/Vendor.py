import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from service import status
from werkzeug.exceptions import NotFound

from flask_sqlalchemy import SQLAlchemy
from service.models.Vendor import Vendor, DataValidationError

from service import app

@app.route("/vendors", methods=["GET"])
def list_vendors():
    app.logger.info("Request for vendor list")
    vendors = []
    vendors = Vendor.all()
    results = [vendor.serialize() for vendor in vendors]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/vendors/<int:vendor_id>", methods=["GET"])
def get_vendors(vendor_id):
    app.logger.info("Request for vendor with id: %s", vendor_id)
    vendor = Vendor.find(vendor_id)
    if not vendor:
        raise NotFound("Vendor with id '{}' was not found.".format(vendor_id))
    return make_response(jsonify(vendor.serialize()), status.HTTP_200_OK)


@app.route("/vendors", methods=["POST"])
def create_vendors():
    app.logger.info("Request to create a vendor")
    check_content_type("application/json")
    vendor = Vendor()
    vendor.deserialize(request.get_json())
    vendor.create()
    message = vendor.serialize()
    location_url = url_for("get_vendors", vendor_id=vendor.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


@app.route("/vendors/<int:vendor_id>", methods=["PUT"])
def update_vendors(vendor_id):
    app.logger.info("Request to update vendor with id: %s", vendor_id)
    check_content_type("application/json")
    vendor = Vendor.find(vendor_id)
    if not vendor:
        raise NotFound("Vendor with id '{}' was not found.".format(vendor_id))
    vendor.deserialize(request.get_json())
    vendor.id = vendor_id
    vendor.save()
    return make_response(jsonify(vendor.serialize()), status.HTTP_200_OK)


@app.route("/vendors/<int:vendor_id>", methods=["DELETE"])
def delete_vendors(vendor_id):
    app.logger.info("Request to delete vendor with id: %s", vendor_id)
    vendor = Vendor.find(vendor_id)
    if vendor:
        vendor.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


@app.route("/vendors/search", methods=["GET"])
def search_vendors():
    app.logger.info("Request for vendor list")
    vendors = []
    email = request.args.get("email")
    name = request.args.get("name")
    phone = request.args.get("phone")

    if email:
        vendors = Vendor.find_by_email(email)
    elif name:
        vendors = Vendor.find_by_name(name)
    elif phone:
        vendors = Vendor.find_by_phone(phone)
 
    results = [vendor.serialize() for vendor in vendors]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/vendors/<int:vendor_id>/make-available")
def available_vendors(vendor_id):
    app.logger.info("Request to make vendor available with id: %s", vendor_id)
    vendor = Vendor.find(vendor_id)
    if not vendor:
        raise NotFound("Vendor with id '{}' was not found.".format(vendor_id))
    vendor.id = vendor_id
    vendor.available = True
    vendor.save()
    return make_response(jsonify(vendor.serialize()), status.HTTP_200_OK)


def check_content_type(content_type):
    if "Content-Type" in request.headers and request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: [%s]", request.headers.get("Content-Type"))
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
