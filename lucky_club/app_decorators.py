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
            raise InvalidUsage('Category does not exists', status_code=400)

    return wrapper

