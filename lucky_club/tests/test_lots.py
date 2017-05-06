import io, os
from flask import json
import lucky_club.api.account.models
import lucky_club.api.attaches.models
import lucky_club.api.categories.models
import lucky_club.api.lots.models
import lucky_club.users_manager.models
from lucky_club import lucky_club
from lucky_club.tests.test_basic import BasicTests


class LotsTest(BasicTests):
    def add_participant_to_lot(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/join-lot'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def leave_lot(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/leave-lot'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def get_messages(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/get-messages'.format(lot_id)

        rv = self.app.get(url,
                          follow_redirects=True,
                          content_type=content_type,
                          headers=headers)
        return rv

    def add_message(self, user_data, message_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/lots/{0}/add-message'.format(lot_id),
                           data=message_data,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def delete_message(self, user_data, message_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/lots/delete-message/{0}'.format(message_id),
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def set_favorite(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/set-favorite'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def get_favorites(self, user_data, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/get-favorites'

        rv = self.app.get(url,
                          follow_redirects=True,
                          content_type=content_type,
                          headers=headers)
        return rv

    def un_delete_lot(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/undelete'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def finish_lot(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}/finish'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def edit_lot(self, user_data, lot_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.put('/api/lots/{0}'.format(lot_id),
                          data=lot_data,
                          follow_redirects=True,
                          content_type=content_type,
                          headers=headers)
        return rv

    def get_lot_by_id_post(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def get_lot_by_id(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}'.format(lot_id)

        rv = self.app.get(url,
                          follow_redirects=True,
                          content_type=content_type,
                          headers=headers)
        return rv

    def publish_lot(self, user_data, lot_id, publish=True, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        if publish:
            url = '/api/lots/{0}/publish-lot'.format(lot_id)
        else:
            url = '/api/lots/{0}/un-publish-lot'.format(lot_id)

        rv = self.app.post(url,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def delete_lot(self, user_data, lot_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        url = '/api/lots/{0}'.format(lot_id)

        rv = self.app.delete(url,
                             follow_redirects=True,
                             content_type=content_type,
                             headers=headers)
        return rv

    def add_lot(self, user_data, lot_data, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/lots/',
                           data=lot_data,
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def get_lots_per_page(self, user_data, page=1):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.get('/api/lots/page/{0}'.format(page),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=headers)
        return rv

    def test_add_publish_unpublish_lots_pagination(self):
        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            #
            # Work with lots
            #

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20
            )

            i = 0
            new_lots = []
            while i < 20:
                rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
                self.assertEqual(rv.status_code, 200, rv.data)

                new_lot = json.loads(rv.data)
                new_lots.append(new_lot)
                i += 1

            for lot_i in new_lots:
                rv = self.publish_lot(self.ordinary_user_data, lot_i['id'], publish=True, content_type='application/json')
                self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lots_per_page(self.ordinary_user_data, page=1)
            self.assertEqual(rv.status_code, 200, rv.data)
            ret_pages = json.loads(rv.data)

            self.assertEqual('total_objects' in ret_pages, True, 'missing field \'total_objects\'')
            self.assertEqual('total_pages' in ret_pages, True, 'missing field \'total_pages\'')
            self.assertEqual('page' in ret_pages, True, 'missing field \'page\'')
            self.assertEqual('objects' in ret_pages, True, 'missing field \'objects\'')
            self.assertEqual('has_next' in ret_pages, True, 'missing field \'has_next\'')
            self.assertEqual('has_prev' in ret_pages, True, 'missing field \'has_prev\'')
            self.assertEqual(len(ret_pages['objects']), lucky_club.app.config['PER_PAGE'], 'We added just one row')

            # unpublished
            for lot_i in new_lots:
                rv = self.publish_lot(self.ordinary_user_data, lot_i['id'], publish=False, content_type='application/json')
                self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lots_per_page(self.ordinary_user_data, page=1)
            self.assertEqual(rv.status_code, 200, rv.data)
            ret_pages = json.loads(rv.data)

            self.assertEqual('total_objects' in ret_pages, True, 'missing field \'total_objects\'')
            self.assertEqual('total_pages' in ret_pages, True, 'missing field \'total_pages\'')
            self.assertEqual('page' in ret_pages, True, 'missing field \'page\'')
            self.assertEqual('objects' in ret_pages, True, 'missing field \'objects\'')
            self.assertEqual('has_next' in ret_pages, True, 'missing field \'has_next\'')
            self.assertEqual('has_prev' in ret_pages, True, 'missing field \'has_prev\'')
            self.assertEqual(ret_pages['total_objects'], 0, 'We added just one row')

            # Incomplete data
            incomplete_lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                price=20
            )

            rv = self.add_lot(self.ordinary_user_data, json.dumps(incomplete_lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

    def test_edit_lots(self):
        category_id = 0
        child_id = 0
        new_lot_of_user = None
        new_lot_of_admin = None

        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20.20
            )

            # Add lots
            rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_user = json.loads(rv.data)
            self.assertEqual(new_lot_of_user['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_user['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_user['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_user['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_user['price'][0]), lot_data['price'], rv.data)

            rv = self.add_lot(self.app_owner_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_admin = json.loads(rv.data)
            self.assertEqual(new_lot_of_admin['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_admin['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_admin['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_admin['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_admin['price'][0]), lot_data['price'], rv.data)

            # drop category with data
            rv = self.delete_category(self.app_owner_user_data, category_id)
            data = json.loads(rv.data)
            self.assertEqual(data['success'], False, rv.data)

            rv = self.delete_category(self.app_owner_user_data, child_id)
            data = json.loads(rv.data)
            self.assertEqual(data['success'], False, rv.data)

            # get lot by id
            rv = self.get_lot_by_id(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.get_lot_by_id(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            # get lot by id post
            rv = self.get_lot_by_id_post(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lot_by_id_post(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lot_by_id_post(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lot_by_id_post(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            # edit lots
            edit_lot_data = dict(
                name='Lot edited',
                description='Lot description edited',
                category_id=child_id,
                count_participants=102,
                price=20.30
            )

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            ret_data = json.loads(rv.data)
            self.assertEqual(ret_data['name'], edit_lot_data['name'], rv.data)
            self.assertEqual(ret_data['description'], edit_lot_data['description'], rv.data)
            self.assertEqual(ret_data['category_id'], edit_lot_data['category_id'], rv.data)
            self.assertEqual(ret_data['count_participants'], edit_lot_data['count_participants'], rv.data)
            self.assertEqual(float(ret_data['price'][0]), edit_lot_data['price'], rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            # publish and edit by user
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.edit_lot(self.app_owner_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            # by admin
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.edit_lot(self.app_owner_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.edit_lot(self.app_owner_user_data, json.dumps(edit_lot_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_admin['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            # delete and edit
            rv = self.delete_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.delete_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            # undelete
            rv = self.un_delete_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.un_delete_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.edit_lot(self.app_owner_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.edit_lot(self.app_owner_user_data, json.dumps(edit_lot_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.edit_lot(self.ordinary_user_data, json.dumps(edit_lot_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)

    def test_favorites(self):
        category_id = 0
        child_id = 0
        new_lot_of_user = None
        new_lot_of_admin = None

        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20.20
            )

            # Add lots
            rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_user = json.loads(rv.data)
            self.assertEqual(new_lot_of_user['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_user['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_user['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_user['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_user['price'][0]), lot_data['price'], rv.data)

            rv = self.add_lot(self.app_owner_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_admin = json.loads(rv.data)
            self.assertEqual(new_lot_of_admin['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_admin['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_admin['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_admin['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_admin['price'][0]), lot_data['price'], rv.data)

            # add to favorites
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lot_by_id_post(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            new_lot_of_admin = json.loads(rv.data)
            rv = self.get_lot_by_id_post(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            new_lot_of_user = json.loads(rv.data)

            # admin user
            rv = self.set_favorite(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.set_favorite(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.app_owner_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 2, rv.data)

            rv = self.set_favorite(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.app_owner_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 1, rv.data)
            self.assertDictEqual(favorites['objects'][0], new_lot_of_admin, rv.data)

            rv = self.set_favorite(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.app_owner_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 0, rv.data)

            # ordinary user
            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 2, rv.data)

            ######################
            # unpublish
            ######################
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 0, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            ######################

            ######################
            # delete
            ######################
            rv = self.delete_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 0, rv.data)

            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            ######################

            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 1, rv.data)
            self.assertDictEqual(favorites['objects'][0], new_lot_of_admin, rv.data)

            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 0, rv.data)

            #####################
            # finished
            #####################
            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.set_favorite(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_favorites(self.ordinary_user_data, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            favorites = json.loads(rv.data)
            self.assertEqual('objects' in favorites, True, rv.data)
            self.assertEqual(len(favorites['objects']), 2, rv.data)

    def test_messages(self):
        category_id = 0
        child_id = 0
        new_lot_of_user = None
        new_lot_of_admin = None

        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20.20
            )

            # Add lots
            rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_user = json.loads(rv.data)
            self.assertEqual(new_lot_of_user['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_user['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_user['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_user['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_user['price'][0]), lot_data['price'], rv.data)

            rv = self.add_lot(self.app_owner_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_admin = json.loads(rv.data)
            self.assertEqual(new_lot_of_admin['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_admin['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_admin['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_admin['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_admin['price'][0]), lot_data['price'], rv.data)

            message_data = dict(
                message='Hello world'
            )
            rv = self.add_message(self.app_owner_user_data, message_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)
            rv = self.add_message(self.app_owner_user_data, message_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            # publish
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            lot_messages = []
            rv = self.add_message(self.app_owner_user_data, json.dumps(message_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['message'], message_data['message'], rv.data)
            lot_messages.append(json.loads(rv.data))
            rv = self.add_message(self.app_owner_user_data, json.dumps(message_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['message'], message_data['message'], rv.data)
            lot_messages.append(json.loads(rv.data))

            rv = self.add_message(self.ordinary_user_data, json.dumps(message_data), new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['message'], message_data['message'], rv.data)
            lot_messages.append(json.loads(rv.data))
            rv = self.add_message(self.ordinary_user_data, json.dumps(message_data), new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['message'], message_data['message'], rv.data)
            lot_messages.append(json.loads(rv.data))

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            ######################
            # unpublish
            ######################
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=False, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            ######################

            ######################
            # delete
            ######################
            rv = self.delete_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 403, rv.data)
            # self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            ######################

            #####################
            # finished
            #####################
            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            # delete messages
            for m in lot_messages:
                rv = self.delete_message(self.ordinary_user_data, m['id'], content_type='application/json')
                self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 2, rv.data)

            for m in lot_messages:
                rv = self.delete_message(self.app_owner_user_data, m['id'], content_type='application/json')
                self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

            rv = self.get_messages(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(len(json.loads(rv.data)['messages']), 0, rv.data)

    def test_participants(self):
        category_id = 0
        child_id = 0
        new_lot_of_user = None
        new_lot_of_admin = None

        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20.20
            )

            # Add lots
            rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_user = json.loads(rv.data)
            self.assertEqual(new_lot_of_user['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_user['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_user['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_user['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_user['price'][0]), lot_data['price'], rv.data)

            rv = self.add_lot(self.app_owner_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_admin = json.loads(rv.data)
            self.assertEqual(new_lot_of_admin['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_admin['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_admin['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_admin['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_admin['price'][0]), lot_data['price'], rv.data)

            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            # publish
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            # test add participant
            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 404, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 404, rv.data)

            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], False, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 404, rv.data)

            rv = self.leave_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            ######################
            # delete
            ######################
            rv = self.delete_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_participant_to_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)
            rv = self.un_delete_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual(json.loads(rv.data)['success'], True, rv.data)

            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            ######################

            #####################
            # finished
            #####################
            rv = self.add_participant_to_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.finish_lot(self.app_owner_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.leave_lot(self.ordinary_user_data, new_lot_of_admin['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

    def add_attach(self, user_data, attach_data, lot_id):
        file_name = 'images/русское имя.jpg'
        base_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(base_dir, file_name), 'rb') as test_img:
            test_img_bytes_io = io.BytesIO(test_img.read())

        attach_data['file'] = (test_img_bytes_io, 'русское имя.jpg')

        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.post('/api/attachments/add-attach/{0}'.format(lot_id),
                           data=attach_data,
                           follow_redirects=True,
                           headers=headers)

        return rv

    def delete_attach(self, user_data, attach_id, content_type='multipart/form-data'):
        rv = self.exchange_token(self.application, user_data)
        self.assertEqual(rv.status_code, 200, rv.status)

        data = json.loads(rv.data)
        headers = {"Authorization": "Bearer " + data['access_token']}

        rv = self.app.delete('/api/attachments/delete-attach/{0}'.format(attach_id),
                           follow_redirects=True,
                           content_type=content_type,
                           headers=headers)
        return rv

    def test_add_attaches_to_lot(self):
        category_id = 0
        child_id = 0
        new_lot_of_user = None
        new_lot_of_admin = None

        with lucky_club.app.app_context():
            self.init_users_and_application()

            parent_cat_data = dict(
                name='Parent',
                description='parent description'
            )

            child_cat_data = dict(
                name='Children',
                description='Children description'
            )

            rv = self.add_category_without_photo(self.app_owner_user_data, parent_cat_data)
            self.assertEqual(rv.status_code, 200, rv.status)
            ret_data = json.loads(rv.data)

            category_id = ret_data["id"]

            rv = self.add_child_category(self.app_owner_user_data, json.dumps(child_cat_data), category_id, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            returned_data = json.loads(rv.data)

            child_id = returned_data['id']

            lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                count_participants=10,
                price=20.20
            )

            # Add lots
            rv = self.add_lot(self.ordinary_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_user = json.loads(rv.data)
            self.assertEqual(new_lot_of_user['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_user['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_user['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_user['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_user['price'][0]), lot_data['price'], rv.data)

            rv = self.add_lot(self.app_owner_user_data, json.dumps(lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            new_lot_of_admin = json.loads(rv.data)
            self.assertEqual(new_lot_of_admin['name'], lot_data['name'], rv.data)
            self.assertEqual(new_lot_of_admin['description'], lot_data['description'], rv.data)
            self.assertEqual(new_lot_of_admin['category_id'], lot_data['category_id'], rv.data)
            self.assertEqual(new_lot_of_admin['count_participants'], lot_data['count_participants'], rv.data)
            self.assertEqual(float(new_lot_of_admin['price'][0]), lot_data['price'], rv.data)

            ##################
            # add picture
            ##################

            request_data = dict(
                description='Hello world'
            )
            rv = self.add_attach(self.ordinary_user_data, request_data, new_lot_of_user['id'])
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.add_attach(self.app_owner_user_data, request_data, new_lot_of_user['id'])
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.get_lot_by_id(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.get_lot_by_id(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.get_lot_by_id_post(self.ordinary_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            self.assertEqual('pictures' in json.loads(rv.data), True, rv.data)
            self.assertEqual(len(json.loads(rv.data)['pictures']), 2, rv.data)
            pictures = json.loads(rv.data)['pictures']

            rv = self.get_lot_by_id_post(self.app_owner_user_data, new_lot_of_user['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.add_attach(self.ordinary_user_data, request_data, new_lot_of_admin['id'])
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.delete_attach(self.ordinary_user_data, pictures[0]['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            # publish
            rv = self.publish_lot(self.ordinary_user_data, new_lot_of_user['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)
            rv = self.publish_lot(self.app_owner_user_data, new_lot_of_admin['id'], publish=True, content_type='application/json')
            self.assertEqual(rv.status_code, 200, rv.data)

            rv = self.add_attach(self.ordinary_user_data, request_data, new_lot_of_user['id'])
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_attach(self.app_owner_user_data, request_data, new_lot_of_user['id'])
            self.assertEqual(rv.status_code, 400, rv.data)

            rv = self.add_attach(self.ordinary_user_data, request_data, new_lot_of_admin['id'])
            self.assertEqual(rv.status_code, 403, rv.data)

            rv = self.delete_attach(self.ordinary_user_data, pictures[1]['id'], content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)


# TODO get unpublished
# TODO get deleted
# TODO get without deleted and unpublished
