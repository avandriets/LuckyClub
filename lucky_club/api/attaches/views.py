"""
View module for working with images
add, delete, get, add-to-favorite, add-user
"""
import os

from flask import Blueprint, request, json, jsonify

from lucky_club.api.attaches.models import Attachment
from lucky_club.api.lots.models import Lot
from lucky_club.app_decorators import is_lot_owner_or_admin
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.helper_utils import is_ascii
from lucky_club.my_oauth2_provider import my_oauth2_provider

blueprint_attachments = Blueprint('attachments', __name__)


@blueprint_attachments.route('/add-attach/<int:lot_id>', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_owner_or_admin
def add_attach(lot_id):
    """
    POST create new lot
    :return:
    """
    lot = Lot.query.get(lot_id)

    if lot.published:
        raise InvalidUsage('Lot already published', status_code=400)

    if request.method == 'POST':

        new_lot = Attachment(user=request.oauth.user, lot_id=lot_id)

        try:
            if hasattr(request, 'data') and request.content_type == 'application/json':
                form_data = json.loads(request.data)
            elif 'multipart/form-data' in request.content_type:
                form_data = request.form
            else:
                db.session.rollback()
                raise InvalidUsage('Incorrect content type.', status_code=500)
        except:
            db.session.rollback()
            raise InvalidUsage('Get post data error.', status_code=500)

        from flask_uploads import UploadNotAllowed
        from lucky_club.lucky_club import uploaded_photos

        try:
            if 'file' in request.files:
                file = request.files['file']

                if file.filename == '':
                    db.session.rollback()
                    raise InvalidUsage('Input file.', status_code=500)

                if not is_ascii(file.filename):
                    name, ext = os.path.splitext(file.filename)
                    name = "1" + ext
                    file.filename = name

                filename = uploaded_photos.save(file)
                new_lot.file_url = filename

        except UploadNotAllowed:
            db.session.rollback()
            raise InvalidUsage('The upload was not allowed', status_code=500)
        else:
            if 'description' not in form_data or not form_data['description'].strip():
                db.session.rollback()
                raise InvalidUsage('Field description is empty', status_code=400)
            description = form_data['description']
            new_lot.description = description

        db.session.add(new_lot)
        db.session.commit()

        new_lot = Lot.query.get(new_lot.id)
        return jsonify(new_lot.serialize)


@blueprint_attachments.route('/delete-attach/<int:attachment_id>', methods=['DELETE'])
@my_oauth2_provider.require_oauth()
def delete_attach(attachment_id):
    """
    lot operations
    :param attachment_id:
    :return:
    """
    # TODO implement delete_attach
    pass
