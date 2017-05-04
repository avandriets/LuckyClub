import io, os
from flask import json
import lucky_club.api.account.models
import lucky_club.api.attaches.models
import lucky_club.api.categories.models
import lucky_club.api.lots.models
import lucky_club.users_manager.models
from lucky_club import lucky_club
from lucky_club.tests.test_basic import BasicTests


class CategoryTest(BasicTests):
    def test_add_get_parent_category_by_admin(self):
        file_name = 'images/русское имя.jpg'
        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.app_owner_user_data)

            data = json.loads(rv.data)

            request_data = dict(
                name='Hello',
                description='World'
            )
            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.post('/api/categories/',
                               data=json.dumps(request_data),
                               follow_redirects=True,
                               content_type='application/json',
                               headers=headers)

            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(original_data['name'], 'Hello', 'Wrong name')
            self.assertEqual(original_data['description'], 'World', 'Wrong description')
            self.assertEqual(original_data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(original_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(original_data['picture_url'], "", 'picture_file have to be empty')

            rv = self.app.get('/api/categories/',
                              follow_redirects=True,
                              content_type='application/json',
                              headers=headers)

            data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertIn('Categories', data, 'Returned data not contain Categories')
            self.assertEqual(len(data['Categories']), 1, 'We added just one row')
            self.assertDictEqual(data['Categories'][0], original_data, 'Added and got data are different')

            # add data with photo category
            base_dir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                test_img_bytes_io = io.BytesIO(test_img.read())

            request_data = dict(
                name='Hello',
                description='World',
                file=(test_img_bytes_io, 'русское имя.jpg')
            )
            rv = self.app.post('/api/categories/', data=request_data, follow_redirects=True, headers=headers)
            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(original_data['name'], 'Hello', 'Wrong name')
            self.assertEqual(original_data['description'], 'World', 'Wrong description')
            self.assertEqual(original_data['parent_id'], None, 'parent_id have to be null')
            self.assertNotEqual(original_data['picture_file'], None, 'picture_file does not have to be null')
            self.assertNotEqual(original_data['picture_url'], "", 'picture_file have to be empty')

            url = original_data['picture_url']
            getfile = self.app.get(url, follow_redirects=True)
            self.assertEqual(getfile.status_code, 200, rv.status)

            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                assert getfile.data == test_img.read()

    def test_get_categories_by_user(self):
        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.app_owner_user_data)

            data = json.loads(rv.data)

            request_data = dict(
                name='Hello',
                description='World'
            )
            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.post('/api/categories/',
                               data=json.dumps(request_data),
                               follow_redirects=True,
                               content_type='application/json',
                               headers=headers)

            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(original_data['name'], 'Hello', 'Wrong name')
            self.assertEqual(original_data['description'], 'World', 'Wrong description')
            self.assertEqual(original_data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(original_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(original_data['picture_url'], "", 'picture_file have to be empty')

            rv = self.exchange_token(self.application, self.ordinary_user_data)
            data = json.loads(rv.data)
            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.get('/api/categories/',
                              follow_redirects=True,
                              content_type='application/json',
                              headers=headers)

            data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertIn('Categories', data, 'Returned data not contain Categories')
            self.assertEqual(len(data['Categories']), 1, 'We added just one row')
            self.assertDictEqual(data['Categories'][0], original_data, 'Added and got data are different')

    def test_add_parent_category_by_user(self):
        with lucky_club.app.app_context():
            self.init_users_and_application()

            rv = self.exchange_token(self.application, self.ordinary_user_data)
            self.assertEqual(rv.status_code, 200, rv.status)

            data = json.loads(rv.data)

            request_data = dict(
                name='Hello',
                description='World'
            )
            headers = {"Authorization": "Bearer " + data['access_token']}

            rv = self.app.post('/api/categories/',
                               data=json.dumps(request_data),
                               follow_redirects=True,
                               content_type='application/json',
                               headers=headers)

            self.assertEqual(rv.status_code, 403, rv.status)

            rv = self.app.get('/api/categories/',
                              follow_redirects=True,
                              content_type='application/json',
                              headers=headers)

            data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertIn('Categories', data, 'Returned data not contain Categories')
            self.assertEqual(len(data['Categories']), 0, 'We added just one row')

            # blocked user test
            self.blocked_user = self.create_user(self.blocked_user_data)
            rv = self.exchange_token(self.application, self.blocked_user_data)
            self.assertEqual(rv.status_code, 403, rv.status)

            request_data = dict(
                name='Hello',
                description='World'
            )
            headers = {"Authorization": "Bearer helloworld"}

            rv = self.app.post('/api/categories/',
                               data=json.dumps(request_data),
                               follow_redirects=True,
                               content_type='application/json',
                               headers=headers)
            self.assertEqual(rv.status_code, 401, rv.status)

    def add_category_with_photo(self, user_owner, category_data):
        rv = self.exchange_token(self.application, user_owner)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/categories/',
                           data=category_data,
                           follow_redirects=True,
                           headers=headers)

        return rv

    def test_delete_category(self):
        file_name = 'images/русское имя.jpg'
        with lucky_club.app.app_context():
            self.init_users_and_application()

            request_data = dict(
                name='Hello',
                description='World'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data)
            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(original_data['name'], 'Hello', 'Wrong name')
            self.assertEqual(original_data['description'], 'World', 'Wrong description')
            self.assertEqual(original_data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(original_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(original_data['picture_url'], "", 'picture_file have to be empty')

            rv = self.get_categories(self.app_owner_user_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            data = json.loads(rv.data)
            self.assertIn('Categories', data, 'Returned data not contain Categories')
            self.assertEqual(len(data['Categories']), 1, 'We added just one row')
            self.assertDictEqual(data['Categories'][0], original_data, 'Added and got data are different')

            rv = self.get_category_by_id(self.app_owner_user_data, original_data['id'])
            self.assertEqual(rv.status_code, 200, rv.status)
            data = json.loads(rv.data)
            self.assertEqual(data['name'], request_data['name'], 'Wrong name')
            self.assertEqual(data['description'], request_data['description'], 'Wrong description')
            self.assertEqual(data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(data['picture_url'], "", 'picture_file have to be empty')

            rv = self.delete_category(self.app_owner_user_data, original_data['id'])
            data = json.loads(rv.data)
            self.assertEqual(data['success'], True, 'Successful deleted')

            #
            # delete by ordinary user
            #
            rv = self.add_category_without_photo(self.app_owner_user_data, request_data)

            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 200, rv.status)
            self.assertEqual(original_data['name'], 'Hello', 'Wrong name')
            self.assertEqual(original_data['description'], 'World', 'Wrong description')
            self.assertEqual(original_data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(original_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(original_data['picture_url'], "", 'picture_file have to be empty')

            rv = self.delete_category(self.ordinary_user_data, original_data['id'])
            self.assertEqual(rv.status_code, 403, rv.status)

    def test_add_category_incomplete_data(self):
        with lucky_club.app.app_context():
            self.init_users_and_application()

            request_data = dict(
                name='Hello'
            )
            request_data1 = dict(
                description='World'
            )

            request_data2 = dict()

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data)
            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 400, original_data)

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data1)
            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 400, original_data)

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data2)
            original_data = json.loads(rv.data)
            self.assertEqual(rv.status_code, 400, original_data)

    def test_edit_category(self):
        file_name = 'images/русское имя.jpg'
        with lucky_club.app.app_context():
            self.init_users_and_application()

            request_data = dict(
                name='Hello',
                description='World'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            edited_data = dict(
                name='Hello nah',
                description='World'
            )

            rv = self.edit_category_by_id(self.app_owner_user_data, json.dumps(edited_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)
            self.assertEqual(returned_data['name'], 'Hello nah', 'Wrong name')
            self.assertEqual(returned_data['description'], 'World', 'Wrong description')
            self.assertEqual(returned_data['parent_id'], None, 'parent_id have to be null')
            self.assertEqual(returned_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(returned_data['picture_url'], "", 'picture_file have to be empty')

            # Add photo
            base_dir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                test_img_bytes_io = io.BytesIO(test_img.read())

            request_data = dict(
                name='Hello',
                description='World',
                file=(test_img_bytes_io, 'русское имя.jpg')
            )

            rv = self.edit_category_by_id(self.app_owner_user_data, request_data, category_id)
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)
            self.assertEqual(returned_data['name'], request_data['name'], 'Wrong name')
            self.assertEqual(returned_data['description'], request_data['description'], 'Wrong description')
            self.assertEqual(returned_data['parent_id'], None, 'parent_id have to be null')
            self.assertNotEqual(returned_data['picture_file'], None, 'picture_file have to be null')
            self.assertNotEqual(returned_data['picture_url'], "", 'picture_file have to be empty')

            url = returned_data['picture_url']
            getfile = self.app.get(url, follow_redirects=True)
            self.assertEqual(getfile.status_code, 200, rv.status)

            with open(os.path.join(base_dir, file_name), 'rb') as test_img:
                assert getfile.data == test_img.read()

    def test_add_child_category(self):
        file_name = 'images/русское имя.jpg'
        with lucky_club.app.app_context():
            self.init_users_and_application()

            request_data = dict(
                name='Parent',
                description='parent description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, request_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            child_category = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_category), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            self.assertEqual(returned_data['name'], child_category['name'], 'Wrong name')
            self.assertEqual(returned_data['description'], child_category['description'], 'Wrong description')
            self.assertEqual(returned_data['parent_id'], category_id, 'parent_id have to be null')
            self.assertEqual(returned_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(returned_data['picture_url'], "", 'picture_file have to be empty')

            child_id = returned_data['id']

            child_category = dict(
                name='Children edited',
                description='Children description edoted'
            )
            rv = self.edit_category_by_id(self.app_owner_user_data, child_category, child_id)
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            self.assertEqual(returned_data['name'], child_category['name'], 'Wrong name')
            self.assertEqual(returned_data['description'], child_category['description'], 'Wrong description')
            self.assertEqual(returned_data['parent_id'], category_id, 'parent_id have to be null')
            self.assertEqual(returned_data['picture_file'], None, 'picture_file have to be null')
            self.assertEqual(returned_data['picture_url'], "", 'picture_file have to be empty')

            # delete parent
            rv = self.delete_category(self.app_owner_user_data, category_id)
            data = json.loads(rv.data)
            self.assertEqual(data['success'], False, rv.data)

            rv = self.delete_category(self.app_owner_user_data, child_id)
            data = json.loads(rv.data)
            self.assertEqual(data['success'], True, rv.data)

            rv = self.delete_category(self.app_owner_user_data, category_id)
            data = json.loads(rv.data)
            self.assertEqual(data['success'], True, rv.data)
