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
import logging, uuid
from functools import wraps
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound, UnsupportedMediaType

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Supplier, DataValidationError

# Import Flask application
from . import app

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response, load UI """
    return app.send_static_file("index.html")


######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Supplier REST API Service',
          description='This is a supplier api server.',
          default='suppliers',
          default_label='Supplier operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          authorizations=authorizations,
          prefix='/api'
         )



# Define the model so that the docs reflect what can be sent
create_model = api.model('Supplier', {
    'name': fields.String(required=True,
                          description='The name of the Supplier'),
    'phone': fields.String(required=True,
                          description='The phone of the supplier'),
    'address': fields.String(required=True,
                          description='The address of the supplier'),
    'product_list': fields.List(fields.Integer, required=True,
                          description='The product list of the supplier'),
    'rating': fields.Float(required=True,
                              description='The rating of the supplier'),
    'available': fields.Boolean(required=True,
                                description='Is the Supplier avaialble?')
})

supplier_model = api.inherit(
    'SupplierModel', 
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


# query string arguments
supplier_args = reqparse.RequestParser()
supplier_args.add_argument('name', type=str, required=False, help='List Suppliers by name')
supplier_args.add_argument('phone', type=str, required=False, help='List Suppliers by phone')
supplier_args.add_argument('address', type=str, required=False, help='List Suppliers by address')
supplier_args.add_argument('rating', type=float, required=False, help='List Suppliers by rating')
supplier_args.add_argument('product_id', type=int, required=False, help='List Suppliers by product id')
supplier_args.add_argument('available', type=inputs.boolean, required=False, help='List Suppliers by availability')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


######################################################################
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401
    return decorated

######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex

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
>>>>>>> main


# Define the model so that the docs reflect what can be sent
create_model = api.model('Supplier', {
    'name': fields.String(required=True,
                          description='The name of the Supplier'),
    'phone': fields.String(required=True,
                          description='The phone of the supplier'),
    'address': fields.String(required=True,
                          description='The address of the supplier'),
    'product_list': fields.List(fields.Integer, required=True,
                          description='The product list of the supplier'),
    'rating': fields.Float(required=True,
                              description='The rating of the supplier'),
    'available': fields.Boolean(required=True,
                                description='Is the Supplier avaialble?')
})

supplier_model = api.inherit(
    'SupplierModel', 
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


# query string arguments
supplier_args = reqparse.RequestParser()
supplier_args.add_argument('name', type=str, required=False, help='List Suppliers by name')
supplier_args.add_argument('phone', type=str, required=False, help='List Suppliers by phone')
supplier_args.add_argument('address', type=str, required=False, help='List Suppliers by address')
supplier_args.add_argument('rating', type=float, required=False, help='List Suppliers by rating')
supplier_args.add_argument('product_id', type=int, required=False, help='List Suppliers by product id')
supplier_args.add_argument('available', type=inputs.boolean, required=False, help='List Suppliers by availability')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


######################################################################
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401
    return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex


######################################################################
#  PATH: /suppliers/{id}
######################################################################
@api.route('/suppliers/<supplier_id>')
@api.param('supplier_id', 'The Supplier identifier')
class SupplierResource(Resource):
    """
    SupplierResource class

    Allows the manipulation of a single Supplier
    GET /suppliers/{id} - Returns a Supplier with the id
    PUT /suppliers/{id} - Update a Supplier with the id
    DELETE /suppliers/{id} -  Deletes a Supplier with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A SUPPLIER
    #------------------------------------------------------------------
    @api.doc('get_suppliers')
    @api.response(404, 'Supplier not found')
    @api.marshal_with(supplier_model)
    def get(self, supplier_id):
        """
        Retrieve a single Supplier

        This endpoint will return a Supplier based on it's id
        """
        app.logger.info("Request to Retrieve a supplier with id [%s]", supplier_id)
        supplier = Supplier.find(supplier_id)
        if not supplier:
            abort(status.HTTP_404_NOT_FOUND, "Supplier with id '{}' was not found.".format(supplier_id))
        return supplier.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING SUPPLIER
    #------------------------------------------------------------------
    @api.doc('update_suppliers', security='apikey')
    @api.response(404, 'Supplier not found')
    @api.response(400, 'The posted Supplier data was not valid')
    @api.expect(supplier_model)
    @api.marshal_with(supplier_model)
    @token_required
    def put(self, supplier_id):
        """
        Update a Supplier

        This endpoint will update a Supplier based the body that is posted
        """
        app.logger.info('Request to Update a supplier with id [%s]', supplier_id)
        supplier = Supplier.find(supplier_id)
        if not supplier:
            abort(status.HTTP_404_NOT_FOUND, "Supplier with id '{}' was not found.".format(supplier_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        supplier.deserialize(data)
        supplier.id = supplier_id
        supplier.update()
        return supplier.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A SUPPLIER
    #------------------------------------------------------------------
    @api.doc('delete_suppliers', security='apikey')
    @api.response(204, 'Supplier deleted')
    @token_required
    def delete(self, supplier_id):
        """
        Delete a Supplier

        This endpoint will delete a Supplier based the id specified in the path
        """
        app.logger.info('Request to Delete a supplier with id [%s]', supplier_id)
        supplier = Supplier.find(supplier_id)
        if supplier:
            supplier.delete()
            app.logger.info('Supplier with id [%s] was deleted', supplier_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /suppliers
######################################################################
@api.route('/suppliers', strict_slashes=False)
class SupplierCollection(Resource):
    """ Handles all interactions with collections of Suppliers """
    #------------------------------------------------------------------
    # LIST ALL SUPPLIERS
    #------------------------------------------------------------------
    @api.doc('list_suppliers')
    @api.expect(supplier_args, validate=True)
    @api.marshal_list_with(supplier_model)
    def get(self):
        """ Returns all of the Suppliers """
        app.logger.info('Request to list Suppliers...')
        suppliers = []
        args = supplier_args.parse_args()
        if args["name"]:
            app.logger.info('Find suppliers by name: %s', args["name"])
            suppliers = Supplier.find_by_name(args["name"])
        elif args["phone"]:
            app.logger.info('Find suppliers with phone number: %s', args["phone"])
            suppliers = Supplier.find_by_phone(args["phone"])
        elif args["address"]:
            app.logger.info('Find suppliers with address: %s', args["address"])
            suppliers = Supplier.find_by_address(args["address"])
        elif args["available"] is not None:
            app.logger.info('Find all suppliers that are available: %s', args["available"])
            suppliers = Supplier.find_by_availability(args["available"])
        elif args["rating"]:
            app.logger.info('Find suppliers with rating greater than: %s', args["rating"])
            suppliers = Supplier.find_by_greater_rating(args["rating"])
        elif args["product_id"]:
            app.logger.info('Find suppliers containing product with id %s in their products', \
                args["product_id"])
            suppliers = Supplier.find_by_product(args["product_id"])
        else:
            app.logger.info('Find all suppliers')
            suppliers = Supplier.all()

        results = [supplier.serialize() for supplier in suppliers]
        return results, status.HTTP_200_OK


    #------------------------------------------------------------------
    # ADD A NEW SUPPLIER
    #------------------------------------------------------------------
    @api.doc('create_suppliers', security='apikey')
    @api.expect(create_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Supplier created successfully')
    @api.marshal_with(supplier_model, code=201)
    @token_required
    def post(self):
        """
        Creates a Supplier
        This endpoint will create a Supplier based the data in the body that is posted
        """
        app.logger.info('Request to Create a Supplier')
        supplier = Supplier()
        app.logger.debug('Payload = %s', api.payload)
        supplier.deserialize(api.payload)
        supplier.create()
        app.logger.info('Supplier with new id [%s] created!', supplier.id)
        location_url = api.url_for(SupplierResource, supplier_id=supplier.id, _external=True)
        return supplier.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /suppliers/{id}/penalize
######################################################################
@api.route('/suppliers/<supplier_id>/penalize')
@api.param('supplier_id', 'The Supplier identifier')
class PenalizeResource(Resource):
    """ Penalize actions on a Supplier """
    @api.doc('penalize_suppliers')
    @api.response(404, 'Supplier not found')
    def put(self, supplier_id):
        """
        Penalize a Supplier
        """
        app.logger.info('Request to penalize a Supplier')
        supplier = Supplier.find(supplier_id)
        if not supplier:
            abort(status.HTTP_404_NOT_FOUND, 'Supplier with id [{}] was not found.'.format(supplier_id))

        if supplier.rating >= 1:
            supplier.rating -= 1
        else:
            supplier.rating = 0

        supplier.update()        
        app.logger.info('Supplier with id [%s] has been penalized!', supplier.id)
        return supplier.serialize(), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Supplier.init_db(app)


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
