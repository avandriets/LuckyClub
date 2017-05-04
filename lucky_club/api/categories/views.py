"""
View module for working with categories
add, delete, get
"""
import os
from flask import Blueprint, request, jsonify, json
from lucky_club.api.categories.models import Category
from lucky_club.api.lots.models import Lot
from lucky_club.app_decorators import is_admin_user, is_category_exists, is_admin_user_arg
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.helper_utils import is_ascii
from lucky_club.my_oauth2_provider import my_oauth2_provider

blueprint_categories = Blueprint('categories', __name__)


@blueprint_categories.route('/', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_admin_user(methods=['POST'])
def add_category():
    """
    POST create new category
    :return:
    """
    if request.method == 'POST':

        category = Category(user=request.oauth.user)
        form_data = None

        try:
            if hasattr(request, 'data') and request.content_type == 'application/json':
                form_data = json.loads(request.data)
            elif 'multipart/form-data' in request.content_type:
                form_data = request.form
            else:
                raise InvalidUsage('Incorrect content type.', status_code=500)
        except:
            raise InvalidUsage('Get post data error.', status_code=500)

        from flask_uploads import UploadNotAllowed
        from lucky_club.lucky_club import uploaded_photos

        try:
            if 'file' in request.files:
                file = request.files['file']

                if file.filename == '':
                    raise InvalidUsage('Input file.', status_code=500)

                if not is_ascii(file.filename):
                    name, ext = os.path.splitext(file.filename)
                    name = "1" + ext
                    file.filename = name

                filename = uploaded_photos.save(file)
                category.picture_file = filename

        except UploadNotAllowed:
            raise InvalidUsage('The upload was not allowed', status_code=500)
        else:
            if 'name' not in form_data:
                raise InvalidUsage('Field name is empty', status_code=400)
            name = form_data['name']
            category.name = name

            if 'description' not in form_data:
                raise InvalidUsage('Field description is empty', status_code=400)
            description = form_data['description']
            category.description = description

            db.session.add(category)
            db.session.commit()

        category = Category.query.get(category.id)
        return jsonify(category.serialize)


@blueprint_categories.route('/', methods=['GET'])
def get_category():
    if request.method == 'GET':
        categories = Category.query.all()
        return jsonify(Categories=[c.serialize for c in categories])


@blueprint_categories.route('/<int:category_id>', methods=['GET'])
@is_category_exists
def get_category_by_id(category_id=None):
    """
    lot operations
    :param category_id:
    :return:
    """
    if request.method == 'GET':
        category = Category.query.get(category_id)
        return jsonify(category.serialize)


def category_edit(category, form_data):
    from flask_uploads import UploadNotAllowed
    from lucky_club.lucky_club import uploaded_photos

    try:
        if 'file' in request.files:
            file = request.files['file']

            if file.filename == '':
                raise InvalidUsage('Input file.', status_code=500)

            if not is_ascii(file.filename):
                name, ext = os.path.splitext(file.filename)
                name = "1" + ext
                file.filename = name

            filename = uploaded_photos.save(file)
            category.picture_file = filename

    except UploadNotAllowed:
        raise InvalidUsage('The upload was not allowed', status_code=500)
    else:
        if 'name' not in form_data:
            raise InvalidUsage('Field name is empty', status_code=400)
        name = form_data['name']
        category.name = name

        if 'description' not in form_data:
            raise InvalidUsage('Field description is empty', status_code=400)
        description = form_data['description']
        category.description = description

    return category


@blueprint_categories.route('/<int:category_id>', methods=['PUT', 'DELETE', 'POST'])
@my_oauth2_provider.require_oauth()
@is_admin_user_arg
@is_category_exists
def edit_category(category_id=None):
    """
    operations with category PUT DELETE POST
    :param category_id:
    :return:
    """

    category = Category.query.get(category_id)
    form_data = None

    if request.method != 'DELETE':
        try:
            if hasattr(request, 'data') and request.content_type == 'application/json':
                form_data = json.loads(request.data)
            elif 'multipart/form-data' in request.content_type:
                form_data = request.form
            else:
                raise InvalidUsage('Incorrect content type.', status_code=500)
        except:
            raise InvalidUsage('Get post data error.', status_code=500)

    if request.method == 'PUT':
        category = category_edit(category, form_data=form_data)
        db.session.add(category)
        db.session.commit()

        category = Category.query.get(category.id)
        return jsonify(category.serialize)

    elif request.method == 'DELETE':
        count_lots = Lot.query.filter_by(category_id=category.id).count()
        count_sub_category = Category.query.filter_by(parent_id=category.id).count()
        if count_sub_category == 0 and count_lots == 0:
            db.session.delete(category)
            db.session.commit()
            return jsonify(dict(success=True))
        else:
            return jsonify(dict(success=False, message='lots or other categories refer on it'))

    elif request.method == 'POST':
        new_category = Category(user=request.oauth.user)
        new_category.parent_id = category.id
        new_category = category_edit(new_category, form_data=form_data)
        db.session.add(new_category)
        db.session.commit()

        new_category = Category.query.get(new_category.id)
        return jsonify(new_category.serialize)
