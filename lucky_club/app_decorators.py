from flask import request

from lucky_club.error_helper import InvalidUsage


def is_admin_user(methods=None):
    def wrap(f):
        def wrapped_f(*args):
            if methods and request.method in methods and request.oauth.user.admin_user != 1:
                raise InvalidUsage('Just admin user can do this.', status_code=403)
            elif not methods and request.oauth.user.admin_user != 1:
                raise InvalidUsage('Just admin user can do this.', status_code=403)

            return f(*args)
        return wrapped_f
    return wrap
