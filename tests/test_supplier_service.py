'''
TEST VENDOR SERVICES
'''
import os
import logging
import unittest
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "mysql+pymysql://root@localhost:3306/my_db"
)

class TestSupplierServer(unittest.TestCase):
    """ TEST SUPPLIER SERVER """
    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ end testing """
        logging.debug("end of testing supplier service")

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ tear down """
        db.session.remove()
        db.drop_all()

    def _create_suppliers(self, count):
        """ Factory method to create suppliers in bulk """
        suppliers = []
        for _ in range(count):
            test_supplier = SupplierFactory()
            resp = self.app.post(
                "/suppliers", json=test_supplier.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test supplier"
            )
            new_supplier = resp.get_json()
            test_supplier.supplier_id = new_supplier["id"]
            suppliers.append(test_supplier)
        return suppliers

    def test_get_supplier_list(self):
        """ Get a list of Suppliers """
        self._create_suppliers(5)
        resp = self.app.get("/suppliers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_supplier(self):
        """ Get a single Supplier """
        # get the id of a supplier
        test_supplier = self._create_suppliers(1)[0]
        resp = self.app.get(
            "/suppliers/{}".format(test_supplier.supplier_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_supplier.name)

    def test_get_supplier_not_found(self):
        """ Get a Supplier thats not found """
        resp = self.app.get("/suppliers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_supplier(self):
        """ Create a new Supplier """
        test_supplier = SupplierFactory()
        logging.debug(test_supplier)
        resp = self.app.post(
            "/suppliers", json=test_supplier.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_supplier = resp.get_json()
        self.assertEqual(new_supplier["name"], test_supplier.name, "Names do not match")
        self.assertEqual(
            new_supplier["email"], test_supplier.email, "Email do not match"
        )
        self.assertEqual(
            new_supplier["phone"], test_supplier.phone, "Phone do not match"
        )
        self.assertEqual(
            new_supplier["address"], test_supplier.address, "Address do not match"
        )
        self.assertEqual(
            new_supplier["available"], test_supplier.available, "Availability does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_supplier = resp.get_json()
        self.assertEqual(new_supplier["name"], test_supplier.name, "Names do not match")
        self.assertEqual(
            new_supplier["email"], test_supplier.email, "Email do not match"
        )
        self.assertEqual(
            new_supplier["phone"], test_supplier.phone, "Phone do not match"
        )
        self.assertEqual(
            new_supplier["address"], test_supplier.address, "Address do not match"
        )
        self.assertEqual(
            new_supplier["available"], test_supplier.available, "Availability does not match"
        )

    def test_create_supplier_no_data(self):
        """ Create a Supplier with missing data """
        resp = self.app.post(
            "/suppliers", json={}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supplier_no_content_type(self):
        """ Create a Supplier with no content type """
        resp = self.app.post("/suppliers")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_supplier(self):
        """ Update an existing Supplier """
        # create a supplier to update
        test_supplier = SupplierFactory()
        resp = self.app.post(
            "/suppliers", json=test_supplier.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the supplier
        new_supplier = resp.get_json()
        logging.debug(new_supplier)
        new_supplier["email"] = "unknown@gmail.com"
        resp = self.app.put(
            "/suppliers/{}".format(new_supplier["id"]),
            json=new_supplier,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_supplier = resp.get_json()
        self.assertEqual(updated_supplier["email"], "unknown@gmail.com")

    def test_delete_supplier(self):
        """ Delete a Supplier """
        test_supplier = self._create_suppliers(1)[0]
        resp = self.app.delete(
            "/suppliers/{}".format(test_supplier.supplier_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/suppliers/{}".format(test_supplier.supplier_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_supplier_list_by_name(self):
        """ test query supplier list by name """
        suppliers = self._create_suppliers(10)
        test_name = suppliers[0].name
        name_suppliers = [supplier for supplier in suppliers if supplier.name == test_name]
        resp = self.app.get(
            "/suppliers", query_string="name={}".format(quote_plus(test_name))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_suppliers))
        # check the data just to be sure
        for supplier in data:
            self.assertEqual(supplier["name"], test_name)

    def test_query_supplier_list_by_email(self):
        """ test query supplier list by email """
        suppliers = self._create_suppliers(10)
        test_email = suppliers[0].email
        name_suppliers = [supplier for supplier in suppliers if supplier.email == test_email]
        resp = self.app.get(
            "/suppliers", query_string="email={}".format(quote_plus(test_email))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_suppliers))
        # check the data just to be sure
        for supplier in data:
            self.assertEqual(supplier["email"], test_email)

    def test_query_supplier_list_by_phone(self):
        """ test query supplier list by phone """
        suppliers = self._create_suppliers(10)
        test_name = suppliers[0].phone
        name_suppliers = [supplier for supplier in suppliers if supplier.phone == test_name]
        resp = self.app.get(
            "/suppliers", query_string="phone={}".format(quote_plus(test_name))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_suppliers))
        # check the data just to be sure
        for supplier in data:
            self.assertEqual(supplier["phone"], test_name)

    def test_query_supplier_make_available(self):
        """ test query supplier make avaiable """
        test_supplier = SupplierFactory()
        test_supplier.available = False
        resp = self.app.post(
            "/suppliers", json=test_supplier.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_supplier = resp.get_json()
        logging.debug(new_supplier)
        resp = self.app.get(
            "/suppliers/{}/make-available".format(new_supplier["id"]),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_supplier = resp.get_json()
        self.assertEqual(updated_supplier["available"], True)
