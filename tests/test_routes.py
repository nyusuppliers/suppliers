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
        # Make sure location header is set. Location is the url to get the data
        # Location is currently not set as get_supplier service has not defined yet
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        
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

    def test_query_suppliers_by_name(self):
        """ Test query suppliers by name"""
        test_suppliers = self._create_suppliers(5)
        test_name = test_suppliers[0].name
        name_suppliers = [supplier for supplier in test_suppliers if supplier.name == test_name]
        resp = self.app.get("/suppliers", query_string="name={}".format(test_name))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_suppliers))
        for supplier in data:
            self.assertEqual(supplier["name"], test_name)
    
    def test_query_by_phone(self):
        """Query Suppliers by phone"""
        suppliers = self._create_suppliers(5)
        test_phone = suppliers[0].phone
        phone_suppliers = [supplier for supplier in suppliers if supplier.phone == test_phone]
        resp = self.app.get("/suppliers", query_string="phone={}".format(test_phone))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        for supplier in data:
            self.assertEqual(supplier['phone'], test_phone)   

    def test_query_by_address(self):
        """Query Suppliers by address"""
        suppliers = self._create_suppliers(5)
        test_address = suppliers[0].address
        address_suppliers = [supplier for supplier in suppliers if supplier.address == test_address]
        resp = self.app.get("/suppliers", query_string="address={}".format(test_address))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(address_suppliers))
        for supplier in data:
            self.assertEqual(supplier['address'], test_address)   

    def test_query_by_available(self):
        """Query Suppliers by available"""
        suppliers = self._create_suppliers(5)
        test_available = suppliers[0].available
        available_suppliers = [supplier for supplier in suppliers if supplier.available == test_available]
        resp = self.app.get("/suppliers", query_string="available={}".format(test_available))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(available_suppliers))
        for supplier in data:
            self.assertEqual(supplier['available'], test_available)   
    
    def test_query_by_rating(self):
        """Query Suppliers by rating"""
        suppliers = self._create_suppliers(5)
        rating_limit = suppliers[0].rating
        rating_suppliers = [supplier for supplier in suppliers if supplier.rating >= rating_limit]
        resp = self.app.get("/suppliers", query_string="rating={}".format(rating_limit))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(rating_suppliers))
        for supplier in data:
            self.assertGreaterEqual(supplier['rating'], rating_limit)


    def test_query_by_product_id(self):
        """ Query Suppliers by product id """
        suppliers = self._create_suppliers(5)
        test_product_id = suppliers[0].product_list[0]
        all_suppliers = [supplier for supplier in suppliers if test_product_id in supplier.product_list]
        resp = self.app.get("/suppliers", query_string="product_id={}".format(test_product_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(all_suppliers))
        for supplier in data:
            self.assertIn(test_product_id, supplier['product_list'])
    
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
        resp = self.app.get('/suppliers/{}'.format(test_suppliers[0].id),content_type='application/json')
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
        test_suppliers = self._create_suppliers(2)
        resp = self.app.get(
            "/suppliers/{}".format(test_suppliers[0].id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], test_suppliers[0].id)
        self.assertEqual(data["name"], test_suppliers[0].name)
        self.assertEqual(data["phone"], test_suppliers[0].phone)
        self.assertEqual(data["address"], test_suppliers[0].address)
        self.assertEqual(data["available"], test_suppliers[0].available)
        self.assertEqual(data["product_list"], test_suppliers[0].product_list)
        self.assertEqual(data["rating"], test_suppliers[0].rating)

    def test_get_supplier_not_found(self):
        """Get a supplier not in the db"""
        resp = self.app.get('/suppliers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_supplier(self):
        """Update a Supplier"""
        test_supplier = self._create_suppliers(5)[0]
        test_supplier.name = "test_update"
        resp = self.app.put('/suppliers/{}'.format(test_supplier.id),
                            json=test_supplier.serialize(), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/suppliers/{}'.format(test_supplier.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'test_update')

    def test_update_supplier_not_found(self):
        """Update a Supplier that does not exist"""
        new_supplier = SupplierFactory()
        resp = self.app.put('/suppliers/0', json=new_supplier.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_penalize_supplier(self):
        """penalize a supplier by ID"""
        test_supplier = self._create_suppliers(5)[0]
        old=test_supplier.rating

        resp = self.app.put(
            "/suppliers/{}/penalize".format(test_supplier.id),
            content_type="application/json",
        )
        #self.assertEqual(resp.status_code, status.HTTP_200_OK)
        penalized_supplier = resp.get_json()
        if old >= 1:
            self.assertEqual(penalized_supplier["rating"], old-1)
        else:
            self.assertEqual(penalized_supplier["rating"], 0)

    def test_add_supplier_in_favorite_list(self):
        """ Test Add supplier in favorite """
        test_supplier = self._create_suppliers(1)
        resp = self.app.post("/suppliers/favorites", json={"supplier_id":test_supplier[0].id})
        self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test supplier"
            )
    def test_get_favorite_suppliers(self):
        """ Test to get all favorite list of suppliers """
        test_suppliers = self._create_suppliers(5)
        for t in test_suppliers:
            resp = self.app.post("/suppliers/favorites", json={"supplier_id":t.id})
        resp = self.app.get("/suppliers/favorites")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)


######################################################################
# Def Helper Functions
######################################################################
    def get_supplier_count(self):
        """return the number of suppliers"""
        resp = self.app.get('/suppliers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug('data = %s', data)
        return len(data)

