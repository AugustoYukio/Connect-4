import ipdb
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from ..entities.DTO import validate_theme_schema, fail_creation_theme_schema


bp_theme = Blueprint('bp_theme', __name__, url_prefix='/theme')


@bp_theme.route('/create', methods=['POST'])
def register():
    try:
        data = request.get_json()
        theme = validate_theme_schema.load(data=data)

    except ValidationError as error:
        # import ipdb;ipdb.set_trace()
        fail = fail_creation_theme_schema.load({'errors': [erro for erro in error.args], 'message': "Fail Creation"})
        return jsonify(fail), 301
    except BadRequest as error:
        fail = fail_creation_theme_schema.load(
            {'error': [{'description': error.description}], 'message': "Fail Creation"})
        return jsonify(fail), 400

    try:
        with current_app.app_context() as ctx:
            ctx.app.db.session.add(theme)
            ctx.app.db.session.commit()
    except Exception as error:
        with current_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_theme_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)],
             'message': "Fail Creation"}
        )
        return jsonify(fail), 500


@bp_theme.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        theme = validate_theme_schema.load(data=data)

    except ValidationError as error:
        # import ipdb;ipdb.set_trace()
        fail = fail_creation_theme_schema.load({'errors': [erro for erro in error.args], 'message': "Fail Creation"})
        return jsonify(fail), 301
    except BadRequest as error:
        fail = fail_creation_theme_schema.load(
            {'error': [{'description': error.description}], 'message': "Fail Creation"})
        return jsonify(fail), 400

    try:
        with current_app.app_context() as ctx:
            ctx.app.db.session.add(theme)
            ctx.app.db.session.commit()
    except Exception as error:
        with current_app.app_context() as ctx:
            ctx.app.db.session.rollback()
            ctx.app.db.session.commit()

        fail = fail_creation_theme_schema.load(
            {'errors': [{n_erro + 1: erro} for n_erro, erro in enumerate(error.orig.args)],
             'message': "Fail Creation"}
        )
        return jsonify(fail), 500
