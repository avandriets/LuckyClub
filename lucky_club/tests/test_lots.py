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

    def test_add_lots(self):
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

            # Incom[lete data
            incomplete_lot_data = dict(
                name='Lot',
                description='Lot description',
                category_id=child_id,
                price=20
            )

            rv = self.add_lot(self.ordinary_user_data, json.dumps(incomplete_lot_data), content_type='application/json')
            self.assertEqual(rv.status_code, 400, rv.data)

# TODO test edit
# TODO test delete
# TODO test delete by owner and not
# TODO add attach
