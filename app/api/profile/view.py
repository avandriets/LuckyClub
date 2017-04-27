from flask import Blueprint, jsonify
from flask import request
from app import InvalidUsage
from app import my_oauth2_provider

blueprint_users = Blueprint('profile', __name__)


@blueprint_users.route('/me', methods=['GET', 'PUT'])
@my_oauth2_provider.require_oauth()
def me():
    # TODO get, edit profile function
    try:
        user = request.oauth.user
        response = jsonify(username=user.name)
        return response
    except:
        raise InvalidUsage('There occurs an error.', status_code=500)


@blueprint_users.route('/get-favorites')
@my_oauth2_provider.require_oauth()
def get_favorites():
    # TODO add get_favorites
    pass


@blueprint_users.route('/get-balance')
@my_oauth2_provider.require_oauth()
def get_balance():
    # TODO add get_favorites
    pass

# @blueprint_users.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def restaurant_handler(id):
#     restaurant = session.query(Restaurant).filter_by(id=id).one()
#     if request.method == 'GET':
#         # RETURN A SPECIFIC RESTAURANT
#         return jsonify(restaurant=restaurant.serialize)
#     elif request.method == 'PUT':
#         # UPDATE A SPECIFIC RESTAURANT
#         address = request.args.get('address')
#         image = request.args.get('image')
#         name = request.args.get('name')
#         if address:
#             restaurant.restaurant_address = address
#         if image:
#             restaurant.restaurant_image = image
#         if name:
#             restaurant.restaurant_name = name
#         session.commit()
#         return jsonify(restaurant=restaurant.serialize)
#
#     elif request.method == 'DELETE':
#         # DELETE A SPECFIC RESTAURANT
#         session.delete(restaurant)
#         session.commit()
#         return "Restaurant Deleted"
