import os
import tempfile
import unittest
from app import create_app
from app.database import init_db


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.db_fd, self.app.config['BASEDIR'] = tempfile.mkstemp()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)

        # self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
        #
        # # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config['BASEDIR'])

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    if __name__ == "__main__":
        unittest.main()