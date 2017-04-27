import os
import tempfile
import unittest
from lucky_club import lucky_club
from lucky_club.database import init_db


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.db_fd, lucky_club.app.config['DATABASE'] = tempfile.mkstemp()
        lucky_club.app.config['TESTING'] = True
        self.app = lucky_club.app.test_client()
        with lucky_club.app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(lucky_club.app.config['DATABASE'])

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    if __name__ == "__main__":
        unittest.main()
