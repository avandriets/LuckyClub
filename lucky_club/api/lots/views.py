"""
View module for working with lots
add, delete, get, add-to-favorite, add-user
"""
from flask import Blueprint, jsonify, request, json, current_app

from lucky_club.api.lots.models import Lot, Participants, Favorite
from lucky_club.app_decorators import is_lot_exists, is_lot_owner
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

        try:
            if 'name' not in form_data or not form_data['name'].strip():
                db.session.rollback()
                raise InvalidUsage('Field name is empty', status_code=400)
            name = form_data['name']
            new_lot.name = name

            if 'description' not in form_data or not form_data['description'].strip():
                db.session.rollback()
                raise InvalidUsage('Field description is empty', status_code=400)
            description = form_data['description']
            new_lot.description = description

            if 'category_id' not in form_data:
                db.session.rollback()
                raise InvalidUsage('Field category is empty', status_code=400)
            category = form_data['category_id']
            new_lot.category_id = int(category)

            if 'count_participants' not in form_data:
                db.session.rollback()
                raise InvalidUsage('Field count_participants is empty', status_code=400)
            count_participants = form_data['count_participants']
            new_lot.count_participants = int(count_participants)

            if 'price' not in form_data:
                db.session.rollback()
                raise InvalidUsage('Field price is empty', status_code=400)
            price = form_data['price']
            new_lot.price = float(price)

        except:
            db.session.rollback()
            raise InvalidUsage('Wrong input data', status_code=400)

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
    lots_pages = Lot.query.paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    return jsonify(total_objects=lots_pages.total,
                   total_pages=lots_pages.pages,
                   page=lots_pages.page,
                   objects=[c.serialize for c in lots_pages.items],
                   has_next=lots_pages.has_next,
                   has_prev=lots_pages.has_prev)


@blueprint_lots.route('/<int:lot_id>', methods=['GET'])
@is_lot_exists
@is_published
def get_lot_by_id(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    lot = Lot.query.get(lot_id)
    return jsonify(lot.serialize)


def lot_edit(edited_lot, form_data):
    try:
        if 'name' not in form_data or not form_data['name'].strip():
            db.session.rollback()
            raise InvalidUsage('Field name is empty', status_code=400)
        name = form_data['name']
        edited_lot.name = name

        if 'description' not in form_data or not form_data['description'].strip():
            db.session.rollback()
            raise InvalidUsage('Field description is empty', status_code=400)
        description = form_data['description']
        edited_lot.description = description

        if 'category_id' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field category is empty', status_code=400)
        category = form_data['category_id']
        edited_lot.category_id = int(category)

        if 'count_participants' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field count_participants is empty', status_code=400)
        count_participants = form_data['count_participants']
        edited_lot.count_participants = int(count_participants)

        if 'price' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field price is empty', status_code=400)
        price = form_data['price']
        edited_lot.price = float(price)
    except:
        db.session.rollback()
        raise InvalidUsage('Wrong input data', status_code=400)


@blueprint_lots.route('/<int:lot_id>', methods=['PUT', 'DELETE'])
@my_oauth2_provider.require_oauth()
@is_lot_exists
@is_lot_owner
@can_edit_lot
def edit_delete_lot(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    editet_lot = Lot.query.get(lot_id)
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
        editet_lot = lot_edit(editet_lot, form_data=form_data)
        db.session.add(editet_lot)
        db.session.commit()

        editet_lot = Lot.query.get(editet_lot.id)
        return jsonify(editet_lot.serialize)

    elif request.method == 'DELETE':
        count_members = Participants.query.filter_by(lot_id=editet_lot.id).count()
        if count_members == 0:
            # db.session.delete(editet_lot)
            editet_lot.deleted = True
            editet_lot.published = False
            db.session.commit()
            return jsonify(dict(success=True))
        else:
            return jsonify(dict(success=False, message='there are joined users.'))


@blueprint_lots.route('/<int:lot_id>/add-to-favorite', methods=['POST'])
@my_oauth2_provider.require_oauth()
@visible
def set_favorite(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    try:
        favorite = Favorite.query.filter_by(lot_id=lot_id, user_id=request.oauth.user.id)
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
        else:
            favorite = Favorite(lot_id=lot_id, user_id=request.oauth.user.id)
            db.session.add(favorite)
            db.session.commit()
        return jsonify(dict(success=True, message='ok'))
    except:
        return jsonify(dict(success=False, message='something went wrong'))


@blueprint_lots.route('/<int:lot_id>/join-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
def join_lot(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement join-lot function
    pass


@blueprint_lots.route('/<int:lot_id>/leave-lot', methods=['POST'])
@my_oauth2_provider.require_oauth()
def leave_lot(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement join-lot function
    pass


@blueprint_lots.route('/<int:lot_id>/get-messages', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_messages(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement lot get_messages function
    pass


@blueprint_lots.route('/<int:lot_id>/add-message', methods=['POST'])
@my_oauth2_provider.require_oauth()
def add_message(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement lot add_message function
    pass
