from functools import wraps
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_header, get_jwt_identity, get_jwt, verify_jwt_in_request

# from back_app.src.utils.responses import resp_notallowed_user
from ..utils.responses import resp_notallowed_user


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return resp_notallowed_user()

        return decorator

    return wrapper
