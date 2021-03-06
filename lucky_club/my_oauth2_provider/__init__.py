import jwt
from jwt import ExpiredSignatureError
from datetime import timedelta, datetime
from flask import Blueprint
from flask_oauthlib.provider import OAuth2Provider
from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage
from lucky_club.jwt_parser import JwtParser
from lucky_club.users_manager.models import current_user, Client, Grant, Token, User

blueprint = Blueprint('my_oauth2_provider', __name__)


class MyOauth2Provider(OAuth2Provider, JwtParser):
    def __init__(self, app=None):
        super().__init__(app=None)
        JwtParser.__init__(self)

        self.blueprint = blueprint

    def _clientgetter(self, client_id):
        return Client.query.filter_by(client_id=client_id).first()

    def _grantgetter(self, client_id, code):
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    def _tokensetter(self, token, request, *args, **kwargs):
        toks = Token.query.filter_by(
            client_id=request.client.client_id,
            user_id=request.user.id
        )

        # make sure that every client has only one token connected to a user
        for t in toks:
            db.session.delete(t)
            db.session.commit()

        expires_in = token.pop('expires_in')
        # expires = datetime.utcnow() + timedelta(seconds=expires_in)
        # TODO change when implement token refresh
        expires = datetime.utcnow() + timedelta(3600*24)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )

        db.session.add(tok)
        db.session.commit()
        return tok

    def _grantsetter(self, client_id, code, request, *args, **kwargs):
        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=current_user(),
            expires=expires
        )
        db.session.add(grant)
        db.session.commit()
        return grant

    def _tokengetter(self, access_token=None, refresh_token=None):
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    def _usergetter(self, username, password, client, request, *args, **kwargs):
        if not hasattr(request, 'jwt_token'):
            raise InvalidUsage('wrong parameter', status_code=500)

        jwt_token = request.jwt_token

        if self.app.config['TESTING']:
            try:
                token = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
            except Exception:
                raise InvalidUsage('JWT token decode problem', status_code=500)
        else:
            try:
                token = self.parse_key(token_data=jwt_token, app=self.app)
            except ExpiredSignatureError:
                raise InvalidUsage('Token expired', status_code=500)

        account = User.query.filter_by(firebase_user_id=token['sub']).one_or_none()
        if account is None:
            account = User(firebase_user_id=token['sub'])
            account.email = token['email']
            account.email_verified = token['email_verified']
            account.name = token.get('name')
            account.photo_url = token.get('picture')

            # TODO change in prod system
            # account.admin_user = 1
            account.admin_user = 0
            db.session.add(account)

            from lucky_club.api.profile.models import Profile
            profile = Profile(user=account, screen_name = account.name)
            db.session.add(profile)

            from lucky_club.api.account.models import Account
            bank_account = Account(user=account)
            db.session.add(bank_account)

            db.session.commit()

        if account and account.blocked == 1:
            raise InvalidUsage('Access denied', status_code=403)

        return account


my_oauth2_provider = MyOauth2Provider()


@blueprint.route('/token', methods=['POST'])
@my_oauth2_provider.token_handler
def my_access_token():
    # You can put extra data to request that return to user
    return None


@blueprint.route('/errors')
@my_oauth2_provider.token_handler
def error_by_oauth():
    raise InvalidUsage('There occurs an error.', status_code=500)
