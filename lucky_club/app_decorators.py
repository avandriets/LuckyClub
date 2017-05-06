from flask import request
from functools import wraps

from lucky_club.error_helper import InvalidUsage


def is_admin_user(methods=None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            if methods and request.method in methods and request.oauth.user.admin_user != 1:
                raise InvalidUsage('Just admin user can do this.', status_code=403)
            elif not methods and request.oauth.user.admin_user != 1:
                raise InvalidUsage('Just admin user can do this.', status_code=403)
            return f(*args, **kwargs)

        return wrapped_f

    return wrap


def is_admin_user_arg(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        if request.oauth.user.admin_user != 1:
            raise InvalidUsage('Just admin user can do this.', status_code=403)
        elif request.oauth.user.admin_user != 1:
            raise InvalidUsage('Just admin user can do this.', status_code=403)

        return function(*args, **kwargs)

    return wrapper


def is_category_exists(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.categories.models import Category
        category = Category.query.get(kwargs['category_id'])

        if category:
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('Category does not exists', status_code=404)

    return wrapper


def is_lot_exists(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.lots.models import Lot
        lot = Lot.query.get(kwargs['lot_id'])

        if lot:
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('Lot does not exists', status_code=404)

    return wrapper


def is_lot_owner_or_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.lots.models import Lot
        lot = Lot.query.get(kwargs['lot_id'])

        if lot and (lot.owner_id == request.oauth.user.id or request.oauth.user.admin_user == 1):
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('You do not have permissions to edit object', status_code=403)

    return wrapper


def is_lot_not_deleted_not_finished(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.lots.models import Lot
        lot = Lot.query.get(kwargs['lot_id'])

        if lot and lot.deleted == False and lot.finished == False:
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('You can not edit finished ot deleted lot', status_code=400)

    return wrapper


def is_published(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.lots.models import Lot
        lot = Lot.query.get(kwargs['lot_id'])

        if lot and lot.published == True:
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('lot does not published yes', status_code=400)

    return wrapper


def is_not_lot_owner_or_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        from lucky_club.api.lots.models import Lot
        lot = Lot.query.get(kwargs['lot_id'])

        if lot and lot.owner_id != request.oauth.user.id and request.oauth.user.admin_user == 0:
            return function(*args, **kwargs)
        else:
            raise InvalidUsage('You do not have permissions to edit object', status_code=404)

    return wrapper
