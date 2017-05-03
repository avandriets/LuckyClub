"""
View module for working with lots
add, delete, get, add-to-favorite, add-user
"""
import os
from flask import Blueprint, request, jsonify, json
from lucky_club.api.categories.models import Category
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.helper_utils import is_ascii
from lucky_club.my_oauth2_provider import my_oauth2_provider

blueprint_categories = Blueprint('categories', __name__)


# TODO add admin user decorator
@blueprint_categories.route('/', methods=['GET', 'POST'])
@my_oauth2_provider.require_oauth()
def category_main():
    """
    POST create new lot
    :return:
    """
    if request.method == 'GET':
        categories = Category.query.all()
        return jsonify(Categories=[c.serialize for c in categories])
    elif request.method == 'POST':

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

        return jsonify(category.serialize)


@blueprint_categories.route('/<int:category_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
@my_oauth2_provider.require_oauth()
def get_category(category_id):
    """
    lot operations
    :param category_id:
    :return:
    """
    # TODO implement get_category
    pass
