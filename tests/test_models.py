"""
Test cases for supplier Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service import app
from service.models import Supplier, DataValidationError, db
from .factories import SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  S U P P L I E R   M O D E L   T E S T   C A S E S
######################################################################
class TestSupplierModel(unittest.TestCase):
    """ Test Cases for Supplier Model """

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

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_serialize_supplier(self):
        """ Test serialize() function in Supplier model """
        supplier = SupplierFactory()
        data = supplier.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], supplier.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], supplier.name)
        self.assertIn("phone", data)
        self.assertEqual(data["phone"], supplier.phone)
        self.assertIn("address", data)
        self.assertEqual(data["address"], supplier.address)
        self.assertIn("available", data)
        self.assertEqual(data["available"], supplier.available)
        self.assertIn("product_list", data)
        self.assertEqual(data["product_list"], supplier.product_list)
        self.assertIn("rating", data)
        self.assertEqual(data["rating"], supplier.rating)

    def test_deserialize_supplier(self):
        """ Test deserialize() function in Supplier model """
        data = {
            "id": 1, 
            "name": 'Graves, Thompson and Pena',
            "phone": '620-179-7652',
            "address": '5312 Danielle Spurs Apt. 017\nNorth James, SD 47183',
            "available": True,
            "product_list": [1,2,4,5],
            "rating": 3.5
        }
        supplier = Supplier()
        supplier.deserialize(data)
        self.assertNotEqual(supplier, None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, 'Graves, Thompson and Pena')
        self.assertEqual(supplier.phone, '620-179-7652')
        self.assertEqual(supplier.address, '5312 Danielle Spurs Apt. 017\nNorth James, SD 47183')
        self.assertEqual(supplier.available, True)
        self.assertEqual(supplier.product_list, [1,2,4,5])
        self.assertEqual(supplier.rating, 3.5)

    def test_find(self):
        """ Test find a supplier by supplier_id"""
        suppliers = SupplierFactory.create_batch(5)
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)

        #Checking if all test records have been created
        self.assertEqual(len(Supplier.all()), 5)
        supplier = Supplier.find(suppliers[3].id)
        self.assertNotEqual(supplier, None)
        self.assertEqual(supplier.id, suppliers[3].id)
        self.assertEqual(supplier.name, suppliers[3].name)
        self.assertEqual(supplier.phone, suppliers[3].phone)
        self.assertEqual(supplier.address, suppliers[3].address)
        self.assertEqual(supplier.available, suppliers[3].available)
        self.assertEqual(supplier.product_list, suppliers[3].product_list)
        self.assertEqual(supplier.rating, suppliers[3].rating)