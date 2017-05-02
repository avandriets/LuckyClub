"""
View module for working with lots
add, delete, get, add-to-favorite, add-user
"""
from flask import Blueprint, jsonify
from lucky_club import my_oauth2_provider
from lucky_club.api.lots.models import Lot
from lucky_club.database import db

blueprint_lots = Blueprint('lots', __name__)


@blueprint_lots.route('/', methods=['POST'])
@my_oauth2_provider.require_oauth()
def create():
    """
    POST create new lot
    :return:
    """
    # TODO implement creating of lot
    pass


@blueprint_lots.route('/page/<int:page>', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_lots(page):
    """
    get lots per pages
    :param page:
    :return:
    """
    # TODO implement return of lots with pagination
    lots = db.session.query(Lot).all()
    return jsonify(Lot=[c.serialize for c in lots])


@blueprint_lots.route('/<int:lot_id>', methods=['GET', 'PUT', 'DELETE'])
@my_oauth2_provider.require_oauth()
def lot_operation(lot_id):
    """
    lot operations
    :param lot_id:
    :return:
    """
    # TODO implement lot operations
    pass


@blueprint_lots.route('/<int:lot_id>/get-pictures', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_lot_pictures(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement lot pictures function
    pass


@blueprint_lots.route('/<int:lot_id>/add-to-favorite', methods=['POST'])
@my_oauth2_provider.require_oauth()
def add_to_favorite(lot_id):
    """
    get lot pictures
    :param lot_id:
    :return:
    """
    # TODO implement add-to-favorite function
    pass


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
