'''
TESTING PRODUCT SERVICES
'''
import os
import logging
import unittest
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import ProductFactory, SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "mysql+pymysql://root@localhost:3306/my_db"
)

class TestProductServer(unittest.TestCase):
    """ test product server """
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
        """ tear down class """
        logging.debug("end testing product service")

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_supplier(self):
        supplier = SupplierFactory()
        supplier.create()
        return supplier.supplier_id


    def _create_products(self, count):
        """ Factory method to create products in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            test_product.supplier_id = self._create_supplier()
            resp = self.app.post(
                "/products", json=test_product.serialize_short(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = resp.get_json()
            test_product.product_id = new_product["id"]
            products.append(test_product)
        return products

    def test_get_product_list(self):
        """ Get a list of Products """
        self._create_products(5)
        resp = self.app.get("/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product(self):
        """ Get a single Product """
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get("/products/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """ Create a new Product """
        test_product = ProductFactory()
        test_product.supplier_id = self._create_supplier()
        logging.debug(test_product)
        resp = self.app.post(
            "/products", json=test_product.serialize_short(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_product = resp.get_json()
        self.assertEqual(new_product["name"], test_product.name, "Names do not match")
        self.assertEqual(
            int(new_product["price"]), int(test_product.price), "Price does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        self.assertEqual(new_product["name"], test_product.name, "Names do not match")
        self.assertEqual(
            int(new_product["price"]), int(test_product.price), "Price does not match"
        )

    def test_create_product_no_data(self):
        """ Create a Product with missing data """
        resp = self.app.post(
            "/products", json={}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """ Create a Product with no content type """
        resp = self.app.post("/products")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_product(self):
        """ Update an existing Product """
        # create a product to update
        test_product = ProductFactory()
        test_product.supplier_id = self._create_supplier()
        resp = self.app.post(
            "/products", json=test_product.serialize_short(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["name"] = "unknown"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["name"], "unknown")

    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete(
            "/products/{}".format(test_product.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/products/{}".format(test_product.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_product_list_by_name(self):
        """ testing product listing by name """
        products = self._create_products(10)
        test_name = products[0].name
        name_products = [product for product in products if product.name == test_name]
        resp = self.app.get(
            "/products", query_string="name={}".format(quote_plus(test_name))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_query_product_list_by_price(self):
        """ testing product listing by price """
        products = self._create_products(10)
        test_name = products[0].price
        name_products = [product for product in products if product.price == test_name]
        resp = self.app.get(
            "/products", query_string="price={}".format(quote_plus(str(test_name)))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["price"], test_name)

    def test_query_product_list_by_supplier(self):
        """ testing product listing by supplier """
        products = self._create_products(10)
        test_name = products[0].supplier_id
        name_products = [product for product in products if product.supplier_id == test_name]
        resp = self.app.get(
            "/products", query_string="supplier_id={}".format(quote_plus(str(test_name)))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["supplier_id"], test_name)

    def test_delete_product_by_supplier(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete(
            "/products/delete-by-supplier/{}".format(test_product.supplier_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/products/{}".format(test_product.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
