import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from . import db
logger = logging.getLogger("flask.app")

class DataValidationError(Exception):
    pass

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "vendor_id": self.vendor_id,
            "vendor":self.vendor.serializeShort()
        }

    def serializeShort(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "vendor_id": self.vendor_id,
        }

    def create(self):
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def save(self):
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.price = data["price"]
            self.vendor_id = data["vendor_id"]
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id):
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name):
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_price(cls, price):
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price)

    @classmethod
    def find_by_vendor(cls, vendor_id):
        logger.info("Processing vendor query for %s ...", vendor_id)
        return cls.query.filter(cls.vendor_id == vendor_id)
    
    @classmethod
    def delete_by_vendor(cls, vendor_id):
        logger.info("Processing products delete by vendor query for %s ...", vendor_id)
        cls.query.filter(cls.vendor_id == vendor_id).delete()
        db.session.commit()
