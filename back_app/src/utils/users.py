from datetime import timedelta
from . import *
from flask_jwt_extended import create_access_token, create_refresh_token
from . import *
from ..entities.DTO import (
    fail_get_user_schema, validate_user_schema, fail_creation_user_schema, input_login_user_schema,
    fail_delete_user_schema, fail_update_user_schema, validate_update_user_schema, success_update_user_schema,
    success_delete_user_schema, success_get_user_schema, success_login_user_schema
)
from ..entities.model.inventory import Inventory

from ..entities.model.user import User
from .messages import MSG_INVALID_CREDENTIALS


def make_login_response(user: User) -> dict:
    acess_token = create_access_token(identity=user.id, expires_delta=timedelta(days=5))

    refresh_token = create_refresh_token(identity=user.id)
    return success_login_user_schema.load({'token': acess_token, 'refresh_token': refresh_token})
    # return success_login_user_schema.load({'token': acess_token, 'refresh_token': refresh_token, 'message': 'success'}


def create_user(ctx_app, data):
    try:
        user = validate_user_schema.load(data=data)
        user.gen_hash()
    except ValidationError as error:
        return fail_creation_user_schema.load({'errors': error.normalized_messages()}), 301
    try:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.add(user)
            ctx.app.db.session.commit()
    except (IntegrityError,) as error:
        with ctx_app.app_context() as ctx:
            ctx.app.db.session.rollback()
        return fail_creation_user_schema.load({'errors': {"IntegrityError": error.orig.args}}), 400
    with ctx_app.app_context() as ctx:
        ctx.app.db.session.add(Inventory(user_id=user.id, theme_id=user.current_theme))
        ctx.app.db.session.commit()

    return make_login_response(user), 201


def authenticate(data):
    user = None
    try:
        # import ipdb;ipdb.set_trace()
        user_schema = input_login_user_schema.load(data=data)

    except ValidationError as error:
        return error, 401

    # import ipdb;ipdb.set_trace()
    user = User.query.filter_by(username=user_schema.get('username')).first()

    if user and user.verify_password(user_schema.get('password')):
        return make_login_response(user)

    return jsonify({
        'message': MSG_INVALID_CREDENTIALS
    }), 401


def get_count_of_admin_users():
    return User.query.filter(User.admin.is_(True)).count()


def find_user(user_id, only_active=True):
    if not user_id:
        return fail_get_user_schema.load({'errors': {1: 'user_id must not be empty'}, 'message': "Fail"})
    try:
        clausule = User.id.is_(user_id)
        if only_active:
            clausule = (User.active.is_(True) & clausule)
        user = User.query.where(clausule).first()
        if user is None:
            return fail_get_user_schema.dump(
                {'errors': {1: 'Not Found'}, 'message': f'User id: {user_id} not found'}
            ), 200
        return success_get_user_schema.dump(user), 200
    except ValidationError as error:
        return fail_get_user_schema.load({'errors': error.normalized_messages()}), 301


def delete_user(ctx_app, user_id, force_delete=False):
    if not user_id:
        return fail_delete_user_schema.load(
            {'message': 'Fail Delete', 'errors': {1: f"User id must not empty."}}
        ), 404
    if not force_delete:
        resut_update = update_user(ctx_app, {'id': user_id, 'active': False}, return_id_only=True)
        if resut_update.get('errors', False):
            return fail_delete_user_schema.load({'message': 'Fail Delete', 'errors': resut_update.get('errors')}), 404
        return success_delete_user_schema.load({'deleted_id': resut_update.get('id')}), 202
    try:
        stmt = delete(User).where(User.id == user_id)
        affected_rows = ctx_app.db.session.execute(stmt)
        if affected_rows.rowcount == 0:
            return fail_delete_user_schema.load(
                {'message': 'Fail Delete', 'errors': {1: f"User id: {user_id} not found"}}
            ), 404
        ctx_app.db.session.commit()
    except ValidationError as error:
        return fail_delete_user_schema.load(
            {'message': 'Fail Delete', 'errors': error.normalized_messages()}
        ), 400

    return success_delete_user_schema.load({'deleted_id': user_id}), 202


def update_user(ctx_app, data, return_id_only=False):
    user_id = data.get('id', None)
    if not user_id:
        return fail_update_user_schema.load({'errors': {1: f"User id must not empty."}}), 404
    try:
        valid_data = validate_update_user_schema.load(data)
    except ValidationError as error:
        return fail_update_user_schema.dump({'errors': error.normalized_messages()}), 400
    try:
        user_id = data.pop('id', None)
        stmt = update(User).where(User.id == user_id).values(**valid_data)
        affected_rows = ctx_app.db.session.execute(stmt)
        if affected_rows.rowcount == 0:
            if return_id_only:
                return fail_update_user_schema.load({'errors': {1: f"User id: {user_id} not found"}})
            return fail_update_user_schema.load({'errors': {1: f"User id: {user_id} not found"}}), 404
    except (IntegrityError,) as error:
        return fail_creation_user_schema.load({'errors': {"IntegrityError": error.orig.args}}), 400
    else:
        ctx_app.db.session.commit()
    if return_id_only:
        return {'id': user_id}
    return success_update_user_schema.load({'updated_id': user_id}), 202
