from werkzeug.exceptions import BadRequest
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import update, select, delete