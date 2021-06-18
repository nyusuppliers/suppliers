import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataValidationError(Exception):
    pass
