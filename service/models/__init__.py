'''
MODELS START
'''
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    '''DATA VALIDATION ERROR CLASS'''
