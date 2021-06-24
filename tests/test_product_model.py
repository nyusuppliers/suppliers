'''
TEST PRODUCT MODEL
'''
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import DataValidationError, db
from service.models.product_model import Product
from service import app
from .factories import ProductFactory, SupplierFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "mysql+pymysql://root@localhost:3306/my_db"
)
class TestProductModel(unittest.TestCase):
    """ Test product model """
    @classmethod
    def setUpClass(cls):
        """ setup function, starting point """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        logging.debug("end testing product model")

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

    def create_supplier(self):
        """ create a dummy supplier """
        supplier = SupplierFactory()
        supplier.create()
        return supplier.supplier_id

    def test_create_a_product(self):
        """ Create a product and assert that it exists """
        product = Product(name="fido", price=123, supplier_id=self.create_supplier())
        self.assertTrue(product is not None)
        self.assertEqual(product.product_id, None)
        self.assertEqual(product.name, "fido")
        self.assertEqual(int(product.price), 123)

    def test_add_a_product(self):
        """ test adding a product """
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="fido", price=123, supplier_id=self.create_supplier())
        self.assertTrue(product is not None)
        self.assertEqual(product.product_id, None)
        product.create()
        self.assertEqual(product.product_id, 1)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_update_a_product(self):
        """ test updating a product """
        product = ProductFactory()
        product.supplier_id = self.create_supplier()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertEqual(product.product_id, 1)
        product.name = "apple"
        original_id = product.product_id
        product.save()
        self.assertEqual(product.product_id, original_id)
        self.assertEqual(product.name, "apple")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].product_id, 1)
        self.assertEqual(products[0].name, "apple")

    def test_delete_a_product(self):
        """ test deleting a product """
        product = ProductFactory()
        product.supplier_id = self.create_supplier()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_serialize_a_product(self):
        """ Test serialization of a Product """
        product = ProductFactory()
        product.supplier_id = self.create_supplier()
        product.create()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.product_id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("price", data)
        self.assertEqual(int(data["price"]), int(product.price))
        self.assertIn("supplier_id", data)
        self.assertEqual(data["supplier_id"], product.supplier_id)

    def test_deserialize_a_product(self):
        """ Test deserialization of a Product """
        data = {
            "id": 1,
            "name": "kitty",
            "price": 123,
            "supplier_id":1
        }
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.product_id, None)
        self.assertEqual(product.name, "kitty")
        self.assertEqual(int(product.price), 123)
        self.assertEqual(product.supplier_id, 1)

    def test_deserialize_missing_data(self):
        """ test deserialize failed, missing data """
        data = {"id": 1, "name": "kitty"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """ test deserialize bad data """
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_product(self):
        """ test finding a product """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.supplier_id = self.create_supplier()
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 3)
        # find the 2nd product in the list
        product = Product.find(products[1].product_id)
        self.assertIsNot(product, None)
        self.assertEqual(product.product_id, products[1].product_id)
        self.assertEqual(product.name, products[1].name)


    def test_find_by_name(self):
        """ test finding a product by name """
        Product(name="fido1", price=123, supplier_id=self.create_supplier()).create()
        Product(name="fido2", price=123, supplier_id=self.create_supplier()).create()
        products = Product.find_by_name("fido1")
        self.assertEqual(products[0].name, "fido1")

    def test_find_by_price(self):
        """ test finding a product by price """
        Product(name="fido1", price=123, supplier_id=self.create_supplier()).create()
        Product(name="fido2", price=124, supplier_id=self.create_supplier()).create()
        products = Product.find_by_price(123)
        self.assertEqual(products[0].name, "fido1")
        self.assertEqual(int(products[0].price), 123)

    def test_find_by_supplier(self):
        """ test finding a product by supplier id """
        v_id = self.create_supplier()
        Product(name="fido1", price=123, supplier_id=v_id).create()
        Product(name="fido2", price=124, supplier_id=self.create_supplier()).create()
        products = Product.find_by_supplier(v_id)
        self.assertEqual(products[0].name, "fido1")
        self.assertEqual(int(products[0].price), 123)
        self.assertEqual(products[0].supplier_id, v_id)

    def test_find_or_404_found(self):
        """ finding product or 404 success """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.supplier_id=self.create_supplier()
            product.create()

        product = Product.find_or_404(products[1].product_id)
        self.assertIsNot(product, None)
        self.assertEqual(product.product_id, products[1].product_id)
        self.assertEqual(product.name, products[1].name)

    def test_find_or_404_not_found(self):
        """ find product failed """
        self.assertRaises(NotFound, Product.find_or_404, 0)
