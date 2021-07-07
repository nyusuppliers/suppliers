"""
Models for Suppliers module

Models
------
Supplier - Suppliers' information used in eCommerce website
Attributes:
-----------
id (int): ID of the supplier
name (string): The name of the supplier
phone (string): The phone number of the supplier
address (string): The address of the supplier
availble (boolean): True for active supplier, False for inactive
product_list (list of int): List of product IDs that the supplier offers
rating (float): Rating given for the supplier overall performance
"""


import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

logger = logging.getLogger("flask.app")
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

##################################################
# class Supplier
##################################################
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

    def create(self):
        """
        Creates a Supplier to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Supplier to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty supplier id")
        db.session.commit()

    def delete(self):
        """
        Removes a supplier from the data store
        """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes a supplier into a dictionary
        """
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
        """
        try:
            self.name = data["name"]
            self.phone = data["phone"]
            self.address = data["address"]
            self.available = data["available"]
            self.product_list = data["product_list"]
            self.rating = data["rating"]
        except KeyError as error:
            raise DataValidationError("Invalid Supplier: Data Missing\n{}".format(error))
        except TypeError as error:
            raise DataValidationError("Invalid Supplier: Type Error\n{}".format(error))
        return self

    @classmethod
    def init_db(cls, app):
        """
        Initializes the database session
        """
        logger.info("Initializing database")
        cls.app = app
        print("inside init_db", app.config["SQLALCHEMY_DATABASE_URI"])
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """
        Returns all of the suppliers in the database
        """
        logger.info("Processing all supplier")
        return cls.query.all()

    @classmethod
    def find(cls, supplier_id):
        """ Finds a supplier by it's ID """
        logger.info("Processing lookup for id %s ...", supplier_id)
        return cls.query.get(supplier_id)

    @classmethod
    def find_or_404(cls, supplier_id):
        """ Find a supplier by it's id """
        logger.info("Processing lookup or 404 for id %s ...", supplier_id)
        return cls.query.get_or_404(supplier_id)

    @classmethod
    def find_by_name(cls, name):
        """
        Returns all suppliers with the given name
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_phone(cls, phone):
        """
        Returns all suppliers with the given phone number
        """
        logger.info("Processing phone number query for %s ...", phone)
        return cls.query.filter(cls.phone == phone)

    @classmethod
    def find_by_address(cls, address):
        """
        Returns all suppliers with the given address

        """
        logger.info("Processing address query for %s ...", address)
        return cls.query.filter(cls.address == address)
    
    @classmethod
    def find_by_availability(cls, available = True):
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_product(cls, product_id):
        """
        Return all suppliers with given produce id
        """
        logger.info("Processing product_id query for %d ...", product_id)
        return cls.query.filter(cls.product_list.contains([product_id])).all()

    @classmethod
    def find_by_greater_rating(cls, rating):
        """
        Return all suppliers with rating grater or equal to given rating
        """
        logger.info("Processing greater or equal rating query for %d ...", rating)
        return cls.query.filter(cls.rating >= rating)
    