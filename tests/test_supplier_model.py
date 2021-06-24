'''
TEST VENDOR MODELS
'''
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import DataValidationError, db
from service.models.supplier_model import Supplier, Gender
from service import app
from .factories import SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "mysql+pymysql://root@localhost:3306/my_db"
)
class TestSupplierModel(unittest.TestCase):
    """ Test Supplier model """
    @classmethod
    def setUpClass(cls):
        """ setup class, starting point """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Supplier.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        logging.debug("end suplier model testing")

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_supplier(self):
        """ Create a supplier and assert that it exists """
        supplier = Supplier(name="fido", email="fido@gmail.com", phone="+123",
            address="abc", available=True, gender=Gender.MALE)
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.supplier_id, None)
        self.assertEqual(supplier.name, "fido")
        self.assertEqual(supplier.email, "fido@gmail.com")
        self.assertEqual(supplier.available, True)
        self.assertEqual(supplier.gender, Gender.MALE)
        self.assertEqual(supplier.address, "abc")
        self.assertEqual(supplier.phone, "+123")
        supplier = Supplier(name="fido", email="fido@gmail.com", phone="+123",
            address="abc", available=False, gender=Gender.FEMALE)
        self.assertEqual(supplier.available, False)
        self.assertEqual(supplier.gender, Gender.FEMALE)

    def test_add_a_supplier(self):
        """ test adding a supplier """
        suppliers = Supplier.all()
        self.assertEqual(suppliers, [])
        supplier = Supplier(name="fido", email="fido@gmail.com", phone="+123",
            address="abc", available=True, gender=Gender.MALE)
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.supplier_id, None)
        supplier.create()
        self.assertEqual(supplier.supplier_id, 1)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)

    def test_update_a_supplier(self):
        """ test update supplier """
        supplier = SupplierFactory()
        logging.debug(supplier)
        supplier.create()
        logging.debug(supplier)
        self.assertEqual(supplier.supplier_id, 1)
        supplier.email = "k9@gmail.com"
        original_id = supplier.supplier_id
        supplier.save()
        self.assertEqual(supplier.supplier_id, original_id)
        self.assertEqual(supplier.email, "k9@gmail.com")
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].supplier_id, 1)
        self.assertEqual(suppliers[0].email, "k9@gmail.com")

    def test_delete_a_supplier(self):
        """ test delete a supplier"""
        supplier = SupplierFactory()
        supplier.create()
        self.assertEqual(len(Supplier.all()), 1)
        # delete the supplier and make sure it isn't in the database
        supplier.delete()
        self.assertEqual(len(Supplier.all()), 0)

    def test_serialize_a_supplier(self):
        """ Test serialization of a Supplier """
        supplier = SupplierFactory()
        data = supplier.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], supplier.supplier_id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], supplier.name)
        self.assertIn("email", data)
        self.assertEqual(data["email"], supplier.email)
        self.assertIn("phone", data)
        self.assertEqual(data["phone"], supplier.phone)
        self.assertIn("address", data)
        self.assertEqual(data["address"], supplier.address)
        self.assertIn("available", data)
        self.assertEqual(data["available"], supplier.available)
        self.assertIn("gender", data)
        self.assertEqual(data["gender"], supplier.gender.name)

    def test_deserialize_a_supplier(self):
        """ Test deserialization of a Supplier """
        data = {
            "id": 1,
            "name": "kitty",
            "email": "cat@gmail.com",
            "phone": "+123",
            "address": "abc",
            "available": True,
            "gender": "FEMALE",
        }
        supplier = Supplier()
        supplier.deserialize(data)
        self.assertNotEqual(supplier, None)
        self.assertEqual(supplier.supplier_id, None)
        self.assertEqual(supplier.name, "kitty")
        self.assertEqual(supplier.email, "cat@gmail.com")
        self.assertEqual(supplier.phone, "+123")
        self.assertEqual(supplier.address, "abc")
        self.assertEqual(supplier.available, True)
        self.assertEqual(supplier.gender, Gender.FEMALE)

    def test_deserialize_missing_data(self):
        """ test deserialize missing data """
        data = {"id": 1, "name": "kitty"}
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_deserialize_bad_data(self):
        """ test deserialize bad data """
        data = "this is not a dictionary"
        supplier = Supplier()
        self.assertRaises(DataValidationError, supplier.deserialize, data)

    def test_find_supplier(self):
        """test find suppleir """
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)
        # make sure they got saved
        self.assertEqual(len(Supplier.all()), 3)
        # find the 2nd supplier in the list
        supplier = Supplier.find(suppliers[1].supplier_id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.supplier_id, suppliers[1].supplier_id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.available, suppliers[1].available)

    def test_find_by_email(self):
        """ test find by email """
        Supplier(name="fido1", email="fido1@gmail.com", phone="+123",
            address="abc", available=True, gender=Gender.MALE).create()
        Supplier(name="fido2", email="fido2@gmail.com", phone="+123",
            address="abc", available=False, gender=Gender.MALE).create()
        suppliers = Supplier.find_by_email("fido1@gmail.com")
        self.assertEqual(suppliers[0].email, "fido1@gmail.com")
        self.assertEqual(suppliers[0].name, "fido1")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_name(self):
        """ test find by name """
        Supplier(name="fido1", email="fido1@gmail.com", phone="+123",
            address="abc", available=True, gender=Gender.MALE).create()
        Supplier(name="fido2", email="fido2@gmail.com", phone="+123",
            address="abc", available=False, gender=Gender.MALE).create()
        suppliers = Supplier.find_by_name("fido1")
        self.assertEqual(suppliers[0].email, "fido1@gmail.com")
        self.assertEqual(suppliers[0].name, "fido1")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_phone(self):
        """ test find by phone """
        Supplier(name="fido1", email="fido1@gmail.com", phone="+456",
            address="abc", available=True, gender=Gender.MALE).create()
        Supplier(name="fido2", email="fido2@gmail.com", phone="+789",
            address="abc", available=False, gender=Gender.MALE).create()
        suppliers = Supplier.find_by_phone("+456")
        self.assertEqual(suppliers[0].email, "fido1@gmail.com")
        self.assertEqual(suppliers[0].phone, "+456")
        self.assertEqual(suppliers[0].name, "fido1")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_availability(self):
        """ test find by avaialbity """
        Supplier(name="fido1", email="fido1@gmail.com", phone="+456",
            address="abc", available=True, gender=Gender.MALE).create()
        Supplier(name="fido2", email="fido2@gmail.com", phone="+789",
            address="abc", available=False, gender=Gender.MALE).create()
        suppliers = Supplier.find_by_availability(True)
        self.assertEqual(suppliers[0].email, "fido1@gmail.com")
        self.assertEqual(suppliers[0].phone, "+456")
        self.assertEqual(suppliers[0].name, "fido1")
        self.assertEqual(suppliers[0].available, True)

    def test_find_by_gender(self):
        """ test find by gender """
        Supplier(name="fido1", email="fido1@gmail.com", phone="+456", address="abc",
            available=True, gender=Gender.MALE).create()
        Supplier(name="fido2", email="fido2@gmail.com", phone="+789", address="abc",
            available=False, gender=Gender.FEMALE).create()
        suppliers = Supplier.find_by_gender(Gender.MALE)
        self.assertEqual(suppliers[0].email, "fido1@gmail.com")
        self.assertEqual(suppliers[0].phone, "+456")
        self.assertEqual(suppliers[0].name, "fido1")
        self.assertEqual(suppliers[0].available, True)

    def test_find_or_404_found(self):
        """ find a supplier or give 404 success """
        suppliers = SupplierFactory.create_batch(3)
        for supplier in suppliers:
            supplier.create()

        supplier = Supplier.find_or_404(suppliers[1].supplier_id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.supplier_id, suppliers[1].supplier_id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.available, suppliers[1].available)

    def test_find_or_404_not_found(self):
        """ find a supplier or give 404 failed """
        self.assertRaises(NotFound, Supplier.find_or_404, 0)
