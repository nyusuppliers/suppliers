"""
Test cases for Supplier Model

Test cases can be run with the following:
  nosetests
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


    def test_deserialize_with_no_name(self):
        """Deserialize a Supplier that has no name"""
        data = {
            "id": 1,
            "phone": '620-179-7652',
            "address": '5312 Danielle Spurs Apt. 017\nNorth James, SD 47183',
            "available": True,
            "product_list": [1,2,4,5],
            "rating": 3.5
        }
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)


    def test_deserialize_with_wrong_type_data(self):
        """Deserialize a Supplier that wrong type data"""
        data = "wrong type data"
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, "string data")

    def test_update(self):
        """
        Test update
        """
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.update)


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

    def test_find_by_name(self):
        """ Test find a supplier by supplier name """
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)

        self.assertEqual(len(Supplier.all()), 3)
        supplier = Supplier.find_by_name(suppliers[1].name)
        self.assertNotEqual(supplier[0], None)
        self.assertEqual(supplier[0].id, suppliers[1].id)
        self.assertEqual(supplier[0].name, suppliers[1].name)
        self.assertEqual(supplier[0].phone, suppliers[1].phone)
        self.assertEqual(supplier[0].address, suppliers[1].address)
        self.assertEqual(supplier[0].available, suppliers[1].available)
        self.assertEqual(supplier[0].product_list, suppliers[1].product_list)
        self.assertEqual(supplier[0].rating, suppliers[1].rating)

    def test_find_by_availability(self):
        """Test find all suppliers with given availability flag"""
        Supplier(name="Graves, Thompson and Pena", phone="620-179-7652", \
            address="5312 Danielle Spurs Apt. 017\nNorth James, SD 47183", \
                available=True, product_list=[1,2,4,5], rating=3.5).create()
        Supplier(name="Rogers, Cabrera and Lee", phone="011-526-6218", \
            address="59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107", \
                available=False, product_list=[1,2,3,5], rating=4.8).create()
        Supplier(name="Perez LLC", phone="6574-477-5210", \
            address="41570 Ashley Manors\nNorth Kevinchester, FL 68266", \
                available=True, product_list=[1,2,3], rating=2.7).create()

        suppliers = Supplier.find_by_availability(False)
        supplier_list = [supplier for supplier in suppliers]
        self.assertEqual(len(supplier_list), 1)

    def test_find_by_product(self):
        """Test find all suppliers with given product id"""
        Supplier(name="Graves, Thompson and Pena", phone="620-179-7652", \
            address="5312 Danielle Spurs Apt. 017\nNorth James, SD 47183", \
                available=True, product_list=[1,2,4,5], rating=3.5).create()
        Supplier(name="Rogers, Cabrera and Lee", phone="011-526-6218", \
            address="59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107", \
                available=False, product_list=[1,2,3,5], rating=4.8).create()
        Supplier(name="Perez LLC", phone="6574-477-5210", \
            address="41570 Ashley Manors\nNorth Kevinchester, FL 68266", \
                available=True, product_list=[1,2,3], rating=2.7).create()

        suppliers = Supplier.find_by_product(4)
        self.assertNotEqual(suppliers[0], None)
        self.assertEqual(suppliers[0].name, "Graves, Thompson and Pena")
        self.assertEqual(suppliers[0].phone, "620-179-7652")
        self.assertEqual(suppliers[0].address, \
            "5312 Danielle Spurs Apt. 017\nNorth James, SD 47183")
        self.assertEqual(suppliers[0].available, True)
        self.assertEqual(suppliers[0].product_list, [1,2,4,5])
        self.assertEqual(suppliers[0].rating, 3.5)

    def test_find_by_greater_rating(self):
        """Test find all suppliers with rating higher than the given rating"""
        Supplier(name="Graves, Thompson and Pena", phone="620-179-7652", \
            address="5312 Danielle Spurs Apt. 017\nNorth James, SD 47183", \
                available=True, product_list=[1,2,4,5], rating=3.5).create()
        Supplier(name="Rogers, Cabrera and Lee", phone="011-526-6218", \
            address="59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107", \
                available=False, product_list=[1,2,3,5], rating=4.8).create()
        Supplier(name="Perez LLC", phone="6574-477-5210", \
            address="41570 Ashley Manors\nNorth Kevinchester, FL 68266", \
                available=True, product_list=[1,2,3], rating=2.7).create()

        suppliers = Supplier.find_by_greater_rating(3.5)
        supplier_list = [supplier for supplier in suppliers]
        self.assertEqual(len(supplier_list), 2)
