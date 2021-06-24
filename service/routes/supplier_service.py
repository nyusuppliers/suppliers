'''
VENDOR ROUTES
'''
from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from service import status
from service.models.supplier_model import Supplier

from service import app

@app.route("/suppliers", methods=["GET"])
def list_suppliers():
    """ list all suppliers """
    app.logger.info("Request for supplier list")
    suppliers = []
    email = request.args.get("email")
    name = request.args.get("name")
    phone = request.args.get("phone")

    if email:
        suppliers = Supplier.find_by_email(email)
    elif name:
        suppliers = Supplier.find_by_name(name)
    elif phone:
        suppliers = Supplier.find_by_phone(phone)
    else:
        suppliers = Supplier.all()
    results = [supplier.serialize() for supplier in suppliers]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/suppliers/<int:supplier_id>", methods=["GET"])
def get_suppliers(supplier_id):
    """ get single supplier by id """
    "TBD"


@app.route("/suppliers", methods=["POST"])
def create_suppliers():
    """ create a supplier """
    "TBD"
    


@app.route("/suppliers/<int:supplier_id>", methods=["PUT"])
def update_suppliers(supplier_id):
    """ update a supplier """
    "TBD"


@app.route("/suppliers/<int:supplier_id>", methods=["DELETE"])
def delete_suppliers(supplier_id):
    """ delete a supplier by id """
    "TBD"

@app.route("/suppliers/<int:supplier_id>/make-available")
def available_suppliers(supplier_id):
    """ mark supplier available """
   "TBD"


def check_content_type(content_type):
    """ check content type """
    if "Content-Type" in request.headers and request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: [%s]", request.headers.get("Content-Type"))
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
