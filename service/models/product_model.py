'''
PRODUCT MODEL
'''
import logging
from . import db, DataValidationError
logger = logging.getLogger("flask.app")

class Product(db.Model):
    ''' PRODUCT MODEL CLASS '''
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), nullable=False)

    def __repr__(self):
        '''  '''
        return "<Product %r id=[%s]>" % (self.name, self.product_id)

    def serialize(self):
        """ serialize product """
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "supplier_id": self.supplier_id,
            "supplier":self.supplier.serialize_short()
        }

    def serialize_short(self):
        """ serialize product without vendor details """
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "supplier_id": self.supplier_id,
        }

    def create(self):
        """ creating product """
        logger.info("Creating %s", self.name)
        self.product_id = None
        db.session.add(self)
        db.session.commit()

    def save(self):
        """ saving product """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ deleting product """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def deserialize(self, data):
        """ deserialize the product """
        try:
            self.name = data["name"]
            self.price = data["price"]
            self.supplier_id = data["supplier_id"]
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " +
                error.args[0]) from DataValidationError
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            ) from DataValidationError
        return self

    @classmethod
    def init_db(cls, app):
        """ initiate tables """
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """ display all records of product table """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """ find a single product """
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id):
        """ find a product or give 404 """
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name):
        """ find product by name """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_price(cls, price):
        """ find product by price """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price)

    @classmethod
    def find_by_supplier(cls, supplier_id):
        """ find product by supplier id """
        logger.info("Processing supplier query for %s ...", supplier_id)
        return cls.query.filter(cls.supplier_id == supplier_id)

    @classmethod
    def delete_by_supplier(cls, supplier_id):
        """ delete all products of a supplier """
        logger.info("Processing products delete by supplier query for %s ...", supplier_id)
        cls.query.filter(cls.supplier_id == supplier_id).delete()
        db.session.commit()
