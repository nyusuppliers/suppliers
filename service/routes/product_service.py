'''
PRODUCT ROUTES
'''
from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound

from service import status
from service.models.product_model import Product
from service import app


@app.route("/products", methods=["GET"])
def list_products():
    """ list all products """
    app.logger.info("Request for products list")
    products = []
    name = request.args.get("name")
    price = request.args.get("price")
    supplier_id = request.args.get("supplier_id")

    if name:
        products = Product.find_by_name(name)
    elif price:
        products = Product.find_by_price(price)
    elif supplier_id:
        products = Product.find_by_supplier(supplier_id)
    else:
        products = Product.all()
    results = [product.serialize() for product in products]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """ get a single product route """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(product_id))
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


@app.route("/products", methods=["POST"])
def create_products():
    """ create a product """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.product_id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """ update a product """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(product_id))
    product.deserialize(request.get_json())
    product.product_id = product_id
    product.save()
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """ delete a product """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

@app.route("/products/delete-by-supplier/<int:supplier_id>", methods=["DELETE"])
def delete_by_supplier(supplier_id):
    """ delete all products by supplier id """
    app.logger.info("Request to delete product with supplier id: %s", supplier_id)
    Product.delete_by_supplier(supplier_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


def check_content_type(content_type):
    """ content type checking """
    if "Content-Type" in request.headers and request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: [%s]", request.headers.get("Content-Type"))
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
