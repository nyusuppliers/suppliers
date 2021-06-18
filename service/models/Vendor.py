import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from . import db
from service.models.Product import Product

logger = logging.getLogger("flask.app")


class DataValidationError(Exception):
    pass


class Gender(Enum):
    Male = 0
    Female = 1
    Unknown = 3



class Vendor(db.Model):
    app = None

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    phone = db.Column(db.String(63), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    gender = db.Column(
        db.Enum(Gender), nullable=False, server_default=(Gender.Unknown.name)
    )
    products = db.relationship('Product', backref='vendor', lazy=True)

    def __repr__(self):
        return "<Vendor %r id=[%s]>" % (self.name, self.id)

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
        Product.delete_by_vendor(self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "available": self.available,
            "address": self.address,
            "gender": self.gender.name,
            "products": [product.serializeShort() for product in self.products]
        }

    def serializeShort(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "available": self.available,
            "address": self.address,
            "gender": self.gender.name,
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.phone = data["phone"]
            self.email = data["email"]
            self.address = data["address"]
            self.available = data["available"]
            self.gender = getattr(Gender, data["gender"])  # create enum from string
        except KeyError as error:
            raise DataValidationError("Invalid vendor: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid vendor: body of request contained bad or no data"
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
        logger.info("Processing all Vendors")
        return cls.query.all()

    @classmethod
    def find(cls, vendor_id):
        logger.info("Processing lookup for id %s ...", vendor_id)
        return cls.query.get(vendor_id)

    @classmethod
    def find_or_404(cls, vendor_id):
        logger.info("Processing lookup or 404 for id %s ...", vendor_id)
        return cls.query.get_or_404(vendor_id)

    @classmethod
    def find_by_name(cls, name):
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_email(cls, email):
        logger.info("Processing email query for %s ...", email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_by_phone(cls, phone):
        logger.info("Processing phone query for %s ...", phone)
        return cls.query.filter(cls.phone == phone)

    @classmethod
    def find_by_availability(cls, available=True):
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_gender(cls, gender=Gender.Unknown):
        logger.info("Processing gender query for %s ...", gender.name)
        return cls.query.filter(cls.gender == gender)
