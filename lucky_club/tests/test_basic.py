import tempfile, unittest, os
from flask import json, jsonify
from lucky_club import lucky_club
from lucky_club.database import db
import lucky_club.users_manager.models
import lucky_club.api.categories.models
import lucky_club.api.lots.models
import lucky_club.api.account.models
import lucky_club.api.attaches.models
from lucky_club.api.profile.models import Profile
from lucky_club.users_manager.models import Client, User
from werkzeug.security import gen_salt
import jwt


class BasicTests(unittest.TestCase):
    def init_users_and_application(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        self.ordinary_user_data = {
            'sub': 'ordinary_user@localhost.com',
            'email': 'ordinary_user@localhost.com',
            'email_verified': True,
            'name': 'ordinary_user',
            'photo_url': '',
            'admin_user': 0,
            'blocked': False
        }

        self.blocked_user_data = {
            'sub': 'blocked_user@localhost.com',
            'email': 'blocked_user@localhost.com',
            'email_verified': True,
            'name': 'blocked_user',
            'photo_url': '',
            'admin_user': 0,
            'blocked': True
        }

        self.user_app_owner = self.create_user(self.app_owner_user_data)
        self.application = self.create_application(self.user_app_owner)

    def setUp(self):
        lucky_club.app.config['TESTING'] = True
        self.db_fd, lucky_club.app.config['BASE_DIR'] = tempfile.mkstemp()
        lucky_club.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + lucky_club.app.config['BASE_DIR']
        lucky_club.app.config['DEBUG'] = False
        self.app = lucky_club.app.test_client()

        with lucky_club.app.app_context():
            db.init_app(lucky_club.app)
            db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(lucky_club.app.config['BASE_DIR'])

    def exchange_token(self, client_app, jwt_token):
        data = dict(
            grant_type='password',
            client_id=client_app.client_id,
            client_secret=client_app.client_secret,
            username='user',
            password='12345',
            jwt_token=jwt.encode(jwt_token, 'secret', algorithm='HS256')
        )
        return self.app.post('/oauth/token', data=data, follow_redirects=True)

    def create_application(self, app_owner):
        # Add application to database
        application = None

        new_application = Client(
            application_name="application",
            application_description="test client application",
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=' '.join([
                'http://localhost:8000/authorized',
                'http://127.0.0.1:8000/authorized',
                'http://127.0.1:8000/authorized',
                'http://127.1:8000/authorized',
            ]),
            _default_scopes='email',
            user_id=app_owner.id,
        )

        db.session.add(new_application)
        db.session.commit()
        application = new_application

        return application

    def create_user(self, user_data):
        # Add user to mock database
        account = None
        try:
            account = User(firebase_user_id=user_data['sub'])
            account.email = user_data['email']
            account.email_verified = user_data['email_verified']
            account.name = user_data['name']
            account.photo_url = user_data['photo_url']
            account.admin_user = user_data['admin_user']
            account.blocked = user_data['blocked']
            db.session.add(account)

            profile = Profile(user=account)
            db.session.add(profile)

            from lucky_club.api.account.models import Account
            bank_account = Account(user=account)
            db.session.add(bank_account)

            db.session.commit()
        except Exception as e:
            print(e)
            pass

        return account

    #
    # Categories helper
    #
    def delete_category(self, user_owner, id):
        rv = self.exchange_token(self.application, user_owner)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.delete('/api/categories/{0}'.format(id),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=headers)

        return rv

    def get_categories(self, user_owner):
        rv = self.exchange_token(self.application, user_owner)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.get('/api/categories/',
                          follow_redirects=True,
                          content_type='application/json',
                          headers=headers)

        return rv

    def add_category_without_photo(self, user_owner, category_data):
        rv = self.exchange_token(self.application, user_owner)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/categories/',
                           data=json.dumps(category_data),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=headers)

        return rv


class ExchangeTokenTest(BasicTests):
    def test_create_admin_user(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }
        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")

    def test_create_application(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }
        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")

    def test_owner_application_exchange_token(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")

            rv = self.exchange_token(self.application, self.app_owner_user_data)
            self.assertEqual(rv.status_code, 200, rv.status)

            # check returned data
            data = json.loads(rv.data)
            self.assertEqual('refresh_token' in data, True, 'missing field \'refresh_token\'')
            self.assertEqual('token_type' in data, True, 'missing field \'token_type\'')
            self.assertEqual('scope' in data, True, 'missing field \'scope\'')
            self.assertEqual('access_token' in data, True, 'missing field \'access_token\'')

    def test_incorrect_jwt_token(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")

            data = dict(
                grant_type='password',
                client_id=self.application.client_id,
                client_secret=self.application.client_secret,
                username='user',
                password='12345',
                jwt_token="wrong token"
            )
            rv = self.app.post('/oauth/token', data=data, follow_redirects=True)
            self.assertEqual(rv.status_code, 500, rv.status)

    def test_ordinary_user_exchange_token(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        ordinary_user_data = {
            'sub': 'ordinary_user@localhost.com',
            'email': 'ordinary_user@localhost.com',
            'email_verified': True,
            'name': 'ordinary_user',
            'photo_url': '',
            'admin_user': 0,
            'blocked': False
        }

        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")

            rv = self.exchange_token(self.application, ordinary_user_data)
            self.assertEqual(rv.status_code, 200, rv.status)

            data = json.loads(rv.data)
            self.assertEqual('refresh_token' in data, True, 'missing field \'refresh_token\'')
            self.assertEqual('token_type' in data, True, 'missing field \'token_type\'')
            self.assertEqual('scope' in data, True, 'missing field \'scope\'')
            self.assertEqual('access_token' in data, True, 'missing field \'access_token\'')

    def test_blocked_user_exchange_token(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        blocked_user_data = {
            'sub': 'blocked_user@localhost.com',
            'email': 'blocked_user@localhost.com',
            'email_verified': True,
            'name': 'blocked_user',
            'photo_url': '',
            'admin_user': 0,
            'blocked': True
        }

        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")

            # blocked_user_data
            blocked_user = self.create_user(blocked_user_data)
            self.assertNotEqual(blocked_user, None, "Can not create blocked_user")
            self.assertNotEqual(blocked_user.user_profile, None, "Can not create blocked_user profile")
            self.assertNotEqual(blocked_user.bank_account, None, "Can not create bank account")

            rv = self.exchange_token(self.application, blocked_user_data)
            self.assertEqual(rv.status_code, 403, rv.status)

            data = json.loads(rv.data)
            self.assertEqual('message' in data, True, 'missing response \'message\'')
            self.assertEqual('status_code' in data, True, 'missing response \'status_code\'')

    def test_blocked_admin_exchange_token(self):
        self.app_owner_user_data = {
            'sub': 'app_owner@localhost.com',
            'email': 'app_owner@localhost.com',
            'email_verified': True,
            'name': 'app_owner',
            'photo_url': '',
            'admin_user': 1,
            'blocked': False
        }

        blocked_admin_user_data = {
            'sub': 'blocked_admin_user@localhost.com',
            'email': 'blocked_admin_user@localhost.com',
            'email_verified': True,
            'name': 'blocked_admin_user',
            'photo_url': '',
            'admin_user': 1,
            'blocked': True
        }

        with lucky_club.app.app_context():
            self.user_app_owner = self.create_user(self.app_owner_user_data)
            self.assertNotEqual(self.user_app_owner, None, "Can not create application owner")
            self.assertNotEqual(self.user_app_owner.user_profile, None, "Can not create owner profile")
            self.assertNotEqual(self.user_app_owner.bank_account, None, "Can not create bank account")

            self.application = self.create_application(self.user_app_owner)
            self.assertNotEqual(self.application, None, "Can not create application")
            # blocked admin user
            blocked_admin_user = self.create_user(blocked_admin_user_data)
            self.assertNotEqual(blocked_admin_user, None, "Can not create blocked_admin_user_data")
            self.assertNotEqual(blocked_admin_user.user_profile, None, "Can not create blocked_admin_user_data profile")
            self.assertNotEqual(blocked_admin_user.bank_account, None, "Can not create bank account")

            rv = self.exchange_token(self.application, blocked_admin_user_data)
            self.assertEqual(rv.status_code, 403, rv.status)

            data = json.loads(rv.data)
            self.assertEqual('message' in data, True, 'missing response \'message\'')
            self.assertEqual('status_code' in data, True, 'missing response \'status_code\'')


if __name__ == "__main__":
    unittest.main()
