from flask import Blueprint, jsonify
from flask import json
from flask import request
from lucky_club.api.profile.models import Profile
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.helper_utils import is_ascii
from lucky_club.my_oauth2_provider import my_oauth2_provider
import os

blueprint_users = Blueprint('profile', __name__)


@blueprint_users.route('/me', methods=['GET', 'PUT'])
@my_oauth2_provider.require_oauth()
def me():
    profile = None
    try:
        profile = Profile.query.filter_by(user=request.oauth.user).first()
    except:
        raise InvalidUsage('Get profile error', status_code=500)

    if request.method == 'GET':
        try:
            return jsonify(profile.serialize)
        except:
            raise InvalidUsage('Get profile error', status_code=500)
    elif request.method == 'PUT':

        form_data = None
        try:
            if hasattr(request, 'data') and request.content_type == 'application/json':
                form_data = json.loads(request.data)
            elif 'multipart/form-data' in request.content_type:
                form_data = request.form
            else:
                raise InvalidUsage('Incorrect content type.', status_code=500)
        except:
            raise InvalidUsage('Cannot get input data.', status_code=500)

        from flask_uploads import UploadNotAllowed
        from lucky_club.lucky_club import uploaded_photos

        try:
            if 'file' in request.files:
                file = request.files['file']

                if file.filename == '':
                    raise InvalidUsage('Input file.', status_code=500)

                from pytils.translit import translify

                if not is_ascii(file.filename):
                    name, ext = os.path.splitext(file.filename)
                    name = "1" + ext
                    file.filename = name

                # file.filename = translify(file.filename)
                filename = uploaded_photos.save(file)
                profile.photo_file_name = filename

        except UploadNotAllowed:
            raise InvalidUsage('The upload was not allowed', status_code=500)
        else:
            if 'first_name' in form_data:
                first_name = form_data['first_name']
                profile.first_name = first_name

            if 'screen_name' in form_data:
                screen_name = form_data['screen_name']
                profile.screen_name = screen_name

            if 'last_name' in form_data:
                last_name = form_data['last_name']
                profile.last_name = last_name

            if 'email' in form_data:
                email = form_data['email']
                profile.email = email

            if 'bank_card' in form_data:
                bank_card = form_data['bank_card']
                profile.bank_card = bank_card

            if 'phone' in form_data:
                phone = form_data['phone']
                profile.phone = phone

            db.session.commit()

        profile = Profile.query.filter_by(user=profile.user).first()
        return jsonify(profile.serialize)

    else:
        raise InvalidUsage('Method does not support.', status_code=405)


@blueprint_users.route('/<int:user_id>', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_user_info(user_id):
    profile = Profile.query.get(user_id)
    if profile:
        jsonify(profile.serialize)
    else:
        raise InvalidUsage('Can not find user.', status_code=404)


@blueprint_users.route('/get-balance')
@my_oauth2_provider.require_oauth()
def get_balance():
    # TODO add get_balance
    pass
