"""
View module for working with lots
add, delete, get, add-to-favorite, add-user
"""
from flask import Blueprint
from app import my_oauth2_provider

blueprint_categories = Blueprint('category', __name__)


@blueprint_categories.route('/', methods=['GET'])
@my_oauth2_provider.require_oauth()
def category_main():
    """
    POST create new lot
    :return:
    """
    # TODO implement creating of category
    pass


@blueprint_categories.route('/<int:category_id>', methods=['GET'])
@my_oauth2_provider.require_oauth()
def get_category(category_id):
    """
    lot operations
    :param category_id:
    :return:
    """
    # TODO implement get_category
    pass
