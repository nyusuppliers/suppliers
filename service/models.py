"""
Models for YourResourceModel

All of the models are stored in this module

Models
-----
Supplier - Supplier information used in eCommerce website

Attributes:
-----
id (int): ID of the supplier
name (string): Name of the supplier
phone (string): Phone number of the supplier
address (string): Address of the supplier
availble (boolean): True for active supplier, False for inactive
product_list (list of ints): List of product_id the supplier offers
rating (float): Rating given to the supplier overall performance
"""
import os
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from retry import retry
from requests import HTTPError

# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 10))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Supplier(db.Model):
    """
    Class that represents a supplier
    """

    app = None

    ##################################################
    # Table Schema
    ##################################################
    _tablename_ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    phone = db.Column(db.String(63), nullable=False)
    address = db.Column(db.String(63), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    product_list = db.Column(ARRAY(db.Integer), nullable=True)
    rating = db.Column(db.Float)

    def __repr__(self):
        return "<Supplier %r id=[%s]>" % (self.name, self.id)

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def create(self):
        """
        Creates a Supplier to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def update(self):
        """
        Updates a Supplier to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty supplier id")
        db.session.commit()

    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def delete(self):
        """ Removes a supplier from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a supplier into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "available": self.available,
            "product_list": self.product_list,
            "rating": self.rating}

    def deserialize(self, data):
        """
        Deserializes a supplier from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.phone = data["phone"]
            self.address = data["address"]
            self.available = data["available"]
            self.product_list = data["product_list"]
            self.rating = data["rating"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid supplier: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid supplier: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        print("inside init_db", app.config["SQLALCHEMY_DATABASE_URI"])
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def all(cls):
        """ Returns all of the suppliers in the database """
        logger.info("Processing all supplier")
        return cls.query.all()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find(cls, supplier_id):
        """ Finds a supplier by it's ID """
        logger.info("Processing lookup for id %s ...", supplier_id)
        return cls.query.get(supplier_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_or_404(cls, supplier_id):
        """ Find a supplier by it's id """
        logger.info("Processing lookup or 404 for id %s ...", supplier_id)
        return cls.query.get_or_404(supplier_id)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_name(cls, name):
        """Returns all suppliers with the given name

        Args:
            name (string): the name of the supplier you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_phone(cls, phone):
        """Returns all suppliers with the given phone number

        """
        logger.info("Processing phone query for %s ...", phone)
        return cls.query.filter(cls.phone == phone)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_address(cls, address):
        """Returns all suppliers with the given address

        """
        logger.info("Processing address query for %s ...", address)
        return cls.query.filter(cls.address == address)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_availability(cls, available = True):
        """ Return all suppliers with given available status """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_product(cls, product_id):
        """ Return all suppliers with given produce id """
        logger.info("Processing product_id query for %d ...", product_id)
        return cls.query.filter(cls.product_list.contains([product_id])).all()

    @classmethod
    @retry(
        HTTPError,
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_greater_rating(cls, rating):
        """Return all suppliers with rating grater than given rating """
        logger.info("Processing greater rating query for %d ...", rating)
        return cls.query.filter(cls.rating >= rating)
    