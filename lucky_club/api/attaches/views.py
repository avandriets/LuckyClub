"""
View module for working with images
add, delete, get, add-to-favorite, add-user
"""
from flask import Blueprint

from lucky_club.my_oauth2_provider import my_oauth2_provider

blueprint_attachments = Blueprint('attachments', __name__)


@blueprint_attachments.route('/', methods=['POST'])
@my_oauth2_provider.require_oauth()
def attachment_main():
    """
    POST create new lot
    :return:
    """
    # TODO implement creating of attachment
    pass


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
