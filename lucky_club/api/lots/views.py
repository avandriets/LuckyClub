"""
View module for working with lots
add, delete, get, add-to-favorite, add-user
"""
from flask import Blueprint, jsonify, request, json, current_app

from lucky_club.api.lots.helper import lot_edit
from lucky_club.api.lots.models import Lot, Participants, Favorite, Messages
from lucky_club.app_decorators import is_lot_exists, is_lot_owner_or_admin, is_lot_not_deleted_not_finished, is_published, is_not_lot_owner_or_admin, is_admin_user_arg
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.my_oauth2_provider import my_oauth2_provider

blueprint_lots = Blueprint('lots', __name__)


@blueprint_lots.route('/', methods=['POST'])
@my_oauth2_provider.require_oauth()
def add_lot():
    """
    POST create new lot
    :return:
    """
    if request.method == 'POST':

        new_lot = Lot(owner=request.oauth.user)
        form_data = None

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

        new_lot = lot_edit(new_lot, form_data=form_data)

        db.session.add(new_lot)
        db.session.commit()

        new_lot = Lot.query.get(new_lot.id)
        return jsonify(new_lot.serialize)


@blueprint_lots.route('/page/<int:page>', methods=['GET'])
def get_lots(page):
    """
    get lots per pages
    :param page:
    :return:
    """

    lots_pages = Lot.query.filter(((Lot.finished == True) | (Lot.published == True)) & (Lot.deleted == False)) \
        .paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)

    return jsonify(total_objects=lots_pages.total,
                   total_pages=lots_pages.pages,
                   page=lots_pages.page,
                   objects=[c.serialize for c in lots_pages.items],
                   has_next=lots_pages.has_next,
                   has_prev=lots_pages.has_prev)


@blueprint_lots.route('/', methods=['GET'])
def get_lots_by_page():
    """
    get lots per pages
    :param page:
    :return:
    """
    lots_pages = Lot.query.filter(((Lot.finished == True) | (Lot.published == True)) & (Lot.deleted == False)) \
        .paginate(error_out=False)

    return jsonify(total_objects=lots_pages.total,
                   total_pages=lots_pages.pages,
                   page=lots_pages.page,
                   objects=[c.serialize for c in lots_pages.items],
                   has_next=lots_pages.has_next,
                   has_prev=lots_pages.has_prev)


@blueprint_lots.route('/<int:lot_id>', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_exists
def get_users_lot_by_id(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    lot = Lot.query.get(lot_id)
    if lot.owner_id == request.oauth.user.id or request.oauth.user.admin_user == 1:
        return jsonify(lot.serialize)
    else:
        if (lot.finished or lot.published) and not lot.deleted:
            return jsonify(lot.serialize)
        else:
            raise InvalidUsage('You can not access to this lot', status_code=403)


@blueprint_lots.route('/<int:lot_id>', methods=['GET'])
# @is_lot_not_deleted_not_finished
@is_published
def get_lot_by_id(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """

    lot = Lot.query.get(lot_id)
    if lot.deleted:
        raise InvalidUsage('You can not access to this lot', status_code=403)

    return jsonify(lot.serialize)


@blueprint_lots.route('/<int:lot_id>', methods=['PUT'])
@my_oauth2_provider.require_oauth()
@is_lot_exists
@is_lot_owner_or_admin
@is_lot_not_deleted_not_finished
def edit_lot(lot_id):
    edited_lot = Lot.query.get(lot_id)

    if edited_lot.published:
        raise InvalidUsage('You can not edit published lot.', status_code=403)

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
        edited_lot = lot_edit(edited_lot, form_data=form_data)
        db.session.commit()

        edited_lot = Lot.query.get(edited_lot.id)
        return jsonify(edited_lot.serialize)


@blueprint_lots.route('/<int:lot_id>', methods=['DELETE'])
@my_oauth2_provider.require_oauth()
@is_lot_owner_or_admin
@is_lot_not_deleted_not_finished
def delete_lot(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    editet_lot = Lot.query.get(lot_id)

    if request.method == 'DELETE':
        count_members = Participants.query.filter_by(lot_id=editet_lot.id).count()
        if count_members == 0:
            # db.session.delete(editet_lot)
            editet_lot.deleted = True
            editet_lot.published = False
            editet_lot.finished = False
            db.session.commit()
            return jsonify(dict(success=True))
        else:
            return jsonify(dict(success=False, message='there are joined users.'))


@blueprint_lots.route('/<int:lot_id>/set-favorite', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_published
def set_favorite(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    try:
        favorite = Favorite.query.filter_by(lot_id=lot_id, user_id=request.oauth.user.id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
        else:
            favorite = Favorite(lot_id=lot_id, user_id=request.oauth.user.id)
            db.session.add(favorite)
            db.session.commit()
        return jsonify(dict(success=True, message='ok'))
    except:
        raise InvalidUsage('Something went wrong.', status_code=500)


@blueprint_lots.route('/<int:lot_id>/join-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_published
@is_not_lot_owner_or_admin
def join_lot(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    participant = Participants.query.filter_by(lot_id=lot_id, participant_id=request.oauth.user.id).first()
    if participant:
        raise InvalidUsage('You are already participant.', status_code=400)

    participant = Participants(lot_id=lot_id, participant_id=request.oauth.user.id)
    db.session.add(participant)
    db.session.commit()

    return jsonify(dict(success=True, message='ok'))


@blueprint_lots.route('/<int:lot_id>/leave-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_published
@is_not_lot_owner_or_admin
def leave_lot(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    lot = Lot.query.get(lot_id)

    if lot.finished or lot.deleted:
        raise InvalidUsage('You can not leave lot.', status_code=400)

    participant = Participants.query.filter_by(lot_id=lot_id, participant_id=request.oauth.user.id).first()
    if not participant:
        raise InvalidUsage('You are not participant.', status_code=400)

    db.session.delete(participant)
    db.session.commit()

    return jsonify(dict(success=True, message='ok'))


@blueprint_lots.route('/<int:lot_id>/get-messages', methods=['GET'])
@is_lot_exists
def get_messages(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """

    lot = Lot.query.get(lot_id)

    if (lot.finished or lot.published) and not lot.deleted:
        messages = Messages.query.filter_by(lot_id=lot_id).all()
        return jsonify(messages=[c.serialize for c in messages])
    else:
        raise InvalidUsage('You can not access to this lot', status_code=403)


@blueprint_lots.route('/<int:lot_id>/add-message', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_published
def add_message(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    if request.method == 'POST':

        new_message = Messages(user=request.oauth.user, lot_id=lot_id)
        form_data = None

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

        try:
            if 'message' not in form_data or not form_data['message'].strip():
                db.session.rollback()
                raise InvalidUsage('Field name is empty', status_code=400)
            message = form_data['message']
            new_message.message = message
        except:
            db.session.rollback()
            raise InvalidUsage('Wrong input data', status_code=400)

        db.session.add(new_message)
        db.session.commit()

        new_message = Messages.query.get(new_message.id)
        return jsonify(new_message.serialize)


@blueprint_lots.route('/delete-message/<int:message_id>', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_admin_user_arg
def delete_message(message_id):
    """

    :param lot_id:
    :param message_id:
    :return:
    """
    try:
        message = Messages.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
    except:
        return jsonify(dict(success=False, message='Something went wrong'))

    return jsonify(dict(success=True, message='ok'))


@blueprint_lots.route('/get-favorites', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_favorites():
    # favorites_lots = Favorite.query.filter_by(user_id=request.oauth.user.id).all()
    favorites_lots = Favorite.query.filter((Favorite.user_id == request.oauth.user.id)
                                           & ((Favorite.lot.has(published=True) | (Favorite.lot.has(finished=True))) & (Favorite.lot.has(deleted=False))))

    return jsonify(objects=[c.lot.serialize for c in favorites_lots])


@blueprint_lots.route('/<int:lot_id>/publish-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_not_deleted_not_finished
@is_lot_owner_or_admin
def publish_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot.published:
        raise InvalidUsage('Lot already published', status_code=400)

    try:
        lot.published = True
        db.session.commit()
        return jsonify(dict(success=True, message='ok'))
    except:
        raise InvalidUsage('Wrong input data', status_code=400)


@blueprint_lots.route('/<int:lot_id>/un-publish-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_owner_or_admin
def un_publish_lot(lot_id):
    lot = Lot.query.get(lot_id)

    if not lot.published:
        raise InvalidUsage('Lot does not published yet', status_code=400)

    count_members = Participants.query.filter_by(lot_id=lot.id).count()
    if count_members == 0:
        lot.published = False
        db.session.commit()
        return jsonify(dict(success=True))


@blueprint_lots.route('/<int:lot_id>/undelete', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_exists
@is_admin_user_arg
def un_delete_lot(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    edited_lot = Lot.query.get(lot_id)

    if not edited_lot.deleted:
        raise InvalidUsage('Unappropriated operation with not deleted lot', status_code=400)

    if request.method == 'POST':
        edited_lot.deleted = False
        edited_lot.published = False
        edited_lot.finished = False
        db.session.commit()
        return jsonify(dict(success=True))


@blueprint_lots.route('/<int:lot_id>/finish', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_exists
@is_admin_user_arg
def finished_lot(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    edited_lot = Lot.query.get(lot_id)

    if edited_lot.deleted or not edited_lot.published:
        raise InvalidUsage('Unappropriated operation with not deleted lot', status_code=400)

    if request.method == 'POST':
        edited_lot.finished = True
        db.session.commit()
        return jsonify(dict(success=True))


@blueprint_lots.route('/get-deleted', methods=['POST'])
@my_oauth2_provider.require_oauth()
def get_deleted():
    lots = Lot.query.filter((Lot.deleted == True) & (Lot.owner == request.oauth.user))
    return jsonify([c.serialize for c in lots])


@blueprint_lots.route('/get-drafts', methods=['POST'])
@my_oauth2_provider.require_oauth()
def get_drafts():
    lots = Lot.query.filter((Lot.published == False) & (Lot.deleted == False) & (Lot.owner == request.oauth.user))
    return jsonify([c.serialize for c in lots])


@blueprint_lots.route('/get-recommend', methods=['GET'])
def get_recommend():
    lots = Lot.query.filter((Lot.recommend == True) & (Lot.published == True) & (Lot.deleted == False))
    return jsonify([c.serialize for c in lots])


@blueprint_lots.route('/<int:lot_id>/set-recommend', methods=['POST'])
@my_oauth2_provider.require_oauth()
@is_lot_not_deleted_not_finished
@is_lot_owner_or_admin
def recommend_lot(lot_id):
    lot = Lot.query.get(lot_id)

    try:
        lot.recommend = not lot.recommend
        db.session.commit()
        return jsonify(dict(success=True, message='ok'))
    except:
        raise InvalidUsage('Wrong input data', status_code=400)