"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from typing import SupportsRound
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import SupplierFactory
from service.models import Supplier, DataValidationError, db
from service import status

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
CONTENT_TYPE_JSON = "application/json"
BASE_URL = "/suppliers"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Supplier.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "E-commerce Supplier REST API Service")

    def test_create_supplier(self):
        """Test create new supplier service call"""
        supplier = SupplierFactory()
        logging.debug(supplier)
        resp = self.app.post(
            BASE_URL, json=supplier.serialize(), content_type=CONTENT_TYPE_JSON
        )
        # Check the response code is 201
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # # Make sure location header is set. Location is the url to get the data
        # # Location is currently not set as get_supplier service has not defined yet
        # location = resp.headers.get("Location", None)
        # self.assertIsNotNone(location)
        
        # Check data correctness 
        new_supplier = resp.get_json()
        self.assertEqual(new_supplier["name"], supplier.name, "Name do not match")
        self.assertEqual(new_supplier["phone"], supplier.phone, "Phone number do not match")
        self.assertEqual(new_supplier["address"], supplier.address, "Address do not match")
        self.assertEqual(new_supplier["available"], supplier.available, "Availability Flag do not match")
        self.assertEqual(new_supplier["product_list"], supplier.product_list, "Product List do not match")
        self.assertEqual(new_supplier["rating"], supplier.rating, "Rating do not match")

    def _create_suppliers(self, count):
        """Factory method to create pets in bulk"""
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post(
                BASE_URL, json=test_supplier.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test supplier"
            )
            new_supplier = resp.get_json()
            test_supplier.id = new_supplier["id"]
            suppliers.append(test_supplier)
        return suppliers

    def test_list_suppliers(self):
        """Get a list of suppliers"""
        self._create_suppliers(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
    
    def test_delete_supplier(self):
        """Create Suppliers """
        test_suppliers = self._create_suppliers(5)
        self.assertEqual(len(test_suppliers), 5)

        """Delete a Supplier """
        resp = self.app.delete('/suppliers/{}'.format(test_suppliers[0].id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        """"Check length of db""" 
        new_count = self.get_supplier_count()
        self.assertEqual(new_count, len(test_suppliers)-1)

        """Check if deleted Should return 404"""
        resp = self.app.get('/suppliers/{}'.format(test_supplier.id),content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_deleted_supplier(self):

        """Create Suppliers """
        test_suppliers = self._create_suppliers(5)
        self.assertEqual(len(test_suppliers), 5)
        """Delete an already deleted Supplier"""
        resp = self.app.delete('/suppliers/{}'.format(0), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        """DB should be unchanged"""
        new_count = self.get_supplier_count()
        self.assertEqual(new_count, len(test_suppliers))

    def test_get_supplier(self):
        """Create Suppliers"""
        self._create_suppliers(2)
        resp = self.app.get('/suppliers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], test_supplier.id)
        self.assertEqual(data["name"], test_supplier.name)
        self.assertEqual(data["phone"], test_supplier.phone)
        self.assertEqual(data["address"], test_supplier.address)
        self.assertEqual(data["available"], test_supplier.available)
        self.assertEqual(data["product_list"], test_supplier.product_list)
        self.assertEqual(data["rating"], test_supplier.rating)

    def test_get_supplier_not_found(self):
        """Get a supplier not in the db"""
        resp = self.app.get('/suppliers/0')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)
        data = resp.get_json()
        logging.debug('data = %s', data)
        self.assertIn('not found', data['message'])

######################################################################
# Def Helper Functions
######################################################################
    def get_supplier_count(self):
        """return the number of suppliers"""
        resp = self.app.get('/suppliers')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        logging.debug('data = %s', data)
        return len(data)

