from flask import json
import lucky_club.api.account.models
import lucky_club.api.attaches.models
import lucky_club.api.categories.models
import lucky_club.api.lots.models
import lucky_club.users_manager.models
from lucky_club import lucky_club
from lucky_club.tests.test_basic import BasicTests


class CategoryTest(BasicTests):
    def test_add_parent_category(self):
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
            self.assertIn('Categories',data, 'Returned data not contain Categories')
            self.assertEqual(len(data['Categories']), 1, 'We added just one row')
            self.assertDictEqual(data['Categories'][0],original_data,'Added and got data are different')