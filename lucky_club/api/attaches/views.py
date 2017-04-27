"""
View module for working with images
add, delete, get, add-to-favorite, add-user
"""
import os
from flask import Blueprint
from flask import request
from werkzeug.utils import secure_filename
from app import InvalidUsage
from app import my_oauth2_provider
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

blueprint_attachments = Blueprint('attachment', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint_attachments.route('/', methods=['POST'])
@my_oauth2_provider.require_oauth()
def attachment_main():
    """
    POST create new lot
    :return:
    """
    # TODO implement creating of attachment
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            raise InvalidUsage('Input file.', status_code=500)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            raise InvalidUsage('Input file.', status_code=500)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # TODO Add file and return JSON


@blueprint_attachments.route('/<int:attachment_id>', methods=['GET', 'DELETE'])
@my_oauth2_provider.require_oauth()
def get_attachment(attachment_id):
    """
    lot operations
    :param attachment_id:
    :return:
    """
    # TODO implement get_attachment
    pass
