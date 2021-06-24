'''
VENDOR MODEL
'''
import logging
from enum import Enum
from service.models.product_model import Product
from . import db, DataValidationError

logger = logging.getLogger("flask.app")


class Gender(Enum):
    """ Gender class """
    MALE = 0
    FEMALE = 1
    UNKNOWN = 3



class Supplier(db.Model):
    """ supplier class """
    app = None

    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    phone = db.Column(db.String(63), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    gender = db.Column(
        db.Enum(Gender), nullable=False, server_default=(Gender.UNKNOWN.name)
    )
    products = db.relationship('Product', backref='supplier', lazy=True)

    def __repr__(self):
        """ """
        return "<Supplier %r id=[%s]>" % (self.name, self.supplier_id)

    def create(self):
        """ creating supplier  """
        logger.info("Creating %s", self.name)
        self.supplier_id = None
        db.session.add(self)
        db.session.commit()

    def save(self):
        """ saving supplier updates to db """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ delete a supplier """
        logger.info("Deleting %s", self.name)
        Product.delete_by_supplier(self.supplier_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ serialize a supplier """
        return {
            "id": self.supplier_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "available": self.available,
            "address": self.address,
            "gender": self.gender.name,
            "products": [product.serialize_short() for product in self.products]
        }

    def serialize_short(self):
        """ short serialization, without product details """
        return {
            "id": self.supplier_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "available": self.available,
            "address": self.address,
            "gender": self.gender.name,
        }

    def deserialize(self, data):
        """ deserialize the supplier """
        try:
            self.name = data["name"]
            self.phone = data["phone"]
            self.email = data["email"]
            self.address = data["address"]
            self.available = data["available"]
            self.gender = getattr(Gender, data["gender"])  # create enum from string
        except KeyError as error:
            raise DataValidationError("Invalid supplier: missing " +
                error.args[0]) from DataValidationError
        except TypeError as error:
            raise DataValidationError(
                "Invalid supplier: body of request contained bad or no data"
            ) from DataValidationError
        return self

    @classmethod
    def init_db(cls, app):
        """ init table in database """
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """ display all suppliers """
        logger.info("Processing all Suppliers")
        return cls.query.all()

    @classmethod
    def find(cls, supplier_id):
        """ find a single supplier """
        logger.info("Processing lookup for id %s ...", supplier_id)
        return cls.query.get(supplier_id)

    @classmethod
    def find_or_404(cls, supplier_id):
        """ find a supplier or give  404"""
        logger.info("Processing lookup or 404 for id %s ...", supplier_id)
        return cls.query.get_or_404(supplier_id)

    @classmethod
    def find_by_name(cls, name):
        """ find supplier by name """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_email(cls, email):
        """ find supplier by email """
        logger.info("Processing email query for %s ...", email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_by_phone(cls, phone):
        """ find supplier by phone number """
        logger.info("Processing phone query for %s ...", phone)
        return cls.query.filter(cls.phone == phone)

    @classmethod
    def find_by_availability(cls, available=True):
        """ find supplier by avaialability """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_gender(cls, gender=Gender.UNKNOWN):
        """ find supplier by gender """
        logger.info("Processing gender query for %s ...", gender.name)
        return cls.query.filter(cls.gender == gender)
