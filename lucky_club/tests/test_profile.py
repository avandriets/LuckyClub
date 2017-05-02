import io, os
from flask import json
import lucky_club.api.account.models
import lucky_club.api.attaches.models
import lucky_club.api.categories.models
import lucky_club.api.lots.models
import lucky_club.users_manager.models
from lucky_club import lucky_club
from lucky_club.tests.test_basic import BasicTests


class UpdateProfileTest(BasicTests):
    def test_get_user_profile(self):
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
            self.application = self.create_application(self.user_app_owner)
            rv = self.exchange_token(self.application, self.app_owner_user_data)

            data = json.loads(rv.data)
            request_data = dict(
                access_token=data['access_token']
            )
            rv = self.app.get('/api/profile/me', data=request_data, follow_redirects=True)
            self.assertEqual(rv.status_code, 200, rv.status)

            rv = self.exchange_token(self.application, ordinary_user_data)
            data = json.loads(rv.data)
            request_data = dict(
                access_token=data['access_token']
            )
            rv = self.app.get('/api/profile/me', data=request_data, follow_redirects=True)
            self.assertEqual(rv.status_code, 200, rv.status)

    def test_delete_post_user_profile(self):
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
            self.application = self.create_application(self.user_app_owner)
            rv = self.exchange_token(self.application, self.app_owner_user_data)

            data = json.loads(rv.data)
            request_data = dict(
                access_token=data['access_token']
            )
            rv = self.app.post('/api/profile/me', data=request_data, follow_redirects=True)
            self.assertEqual(rv.status_code, 405, rv.status)

            rv = self.app.delete('/api/profile/me', data=request_data, follow_redirects=True)
            self.assertEqual(rv.status_code, 405, rv.status)

    def test_incorrect_token_access_user_profile(self):
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
            self.application = self.create_application(self.user_app_owner)
            rv = self.exchange_token(self.application, self.app_owner_user_data)

            request_data = dict(
                access_token='incorrect token'
            )
            rv = self.app.get('/api/profile/me', data=request_data, follow_redirects=True)
            self.assertEqual(rv.status_code, 401, rv.status)

    def test_put_json_data_user_profile(self):
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
            self.application = self.create_application(self.user_app_owner)
            rv = self.exchange_token(self.application, self.app_owner_user_data)

            data = json.loads(rv.data)
            request_data = dict(
                first_name='Иван',
                last_name='Иванов',
            )

            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.put('/api/profile/me',
                              data=json.dumps(request_data),
                              follow_redirects=True,
                              headers=headers,
                              content_type='application/json')

            self.assertEqual(rv.status_code, 200, rv.status)
            data = json.loads(rv.data)
            self.assertEqual('first_name' in data, True, 'missing field \'first_name\'')
            self.assertEqual('last_name' in data, True, 'missing field \'last_name\'')

            self.assertEqual(data['first_name'], 'Иван', 'Wrong first name')
            self.assertEqual(data['last_name'], 'Иванов', 'Wrong last name')

            # check user
            rv = self.exchange_token(self.application, ordinary_user_data)

            data = json.loads(rv.data)
            request_data = dict(
                first_name='Петр',
                last_name='ПетровПетров',
            )
            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.put('/api/profile/me', data=json.dumps(request_data),
                              follow_redirects=True, headers=headers, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.status)
            data = json.loads(rv.data)
            self.assertEqual('first_name' in data, True, 'missing field \'first_name\'')
            self.assertEqual('last_name' in data, True, 'missing field \'last_name\'')
            self.assertEqual(data['first_name'], 'Петр', 'Wrong first name')
            self.assertEqual(data['last_name'], 'ПетровПетров', 'Wrong last name')

    def test_put_photo_latin_filename_user_profile(self):
        file_name = 'images/image_file.jpg'
        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.ordinary_user_data)

            base_dir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                test_img_bytes_io = io.BytesIO(test_img.read())

            data = json.loads(rv.data)

            request_data = dict(
                first_name='Иван',
                last_name='Иванов',
                file=(test_img_bytes_io, 'image_file.jpg')
            )

            headers = {"Authorization": "Bearer " + data['access_token']}
            rv = self.app.put('/api/profile/me', data=request_data, follow_redirects=True, headers=headers)

            data = json.loads(rv.data)

            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(data['first_name'], 'Иван', 'Wrong first name')
            self.assertEqual(data['last_name'], 'Иванов', 'Wrong last name')

            url = data['photo_url']
            getfile = self.app.get(url, follow_redirects=True)
            self.assertEqual(getfile.status_code, 200, rv.status)
            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                assert getfile.data == test_img.read()

    def test_put_photo_russian_filename_user_profile(self):
        file_name = 'images/русское имя.jpg'

        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.ordinary_user_data)

            base_dir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                test_img_bytes_io = io.BytesIO(test_img.read())

            data = json.loads(rv.data)

            request_data = dict(
                first_name='Иван',
                last_name='Иванов',
                file=(test_img_bytes_io, 'русское имя.jpg')
            )

            headers = {"Authorization": "Bearer " + data['access_token']}
            rv = self.app.put('/api/profile/me', data=request_data, follow_redirects=True, headers=headers)

            data = json.loads(rv.data)

            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(data['first_name'], 'Иван', 'Wrong first name')
            self.assertEqual(data['last_name'], 'Иванов', 'Wrong last name')

            url = data['photo_url']
            getfile = self.app.get(url, follow_redirects=True)
            self.assertEqual(getfile.status_code, 200, rv.status)

            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                assert getfile.data == test_img.read()

    def test_put_without_filename_user_profile(self):
        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.ordinary_user_data)

            data = json.loads(rv.data)

            request_data = dict(
                first_name='Иван',
                last_name='Иванов',
            )

            headers = {"Authorization": "Bearer " + data['access_token'],
                       "content-type": 'multipart/form-data'}
            rv = self.app.put('/api/profile/me', data=request_data, follow_redirects=True, headers=headers)

            data = json.loads(rv.data)

            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(data['first_name'], 'Иван', 'Wrong first name')
            self.assertEqual(data['last_name'], 'Иванов', 'Wrong last name')
