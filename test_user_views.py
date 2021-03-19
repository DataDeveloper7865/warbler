"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from flask_wtf import FlaskForm


from models import db, connect_db, Message, User
# from env import USER_POSTGRES, PASSWORD_POSTGRES

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# windows config
# os.environ['DATABASE_URL'] = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@127.0.0.1/warbler_test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.u1 = User.signup(username="testuser1",
                              email="test1@test.com",
                              password="testuser1",
                              image_url=None)

        self.u2 = User.signup(username="testuser2",
                              email="test2@test.com",
                              password="testuser2",
                              image_url=None)

        # self.u3 = User.signup(username="testuser3",
        #                       email="test3@test.com",
        #                       password="testuser3",
        #                       image_url=None)

        db.session.add(self.u1, self.u2)
        db.session.commit()

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result

    # @app.route('/users/<int:user_id>/following')

    def test_show_following(self):
        # u2 follows u1

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            self.u1.following.append(self.u2)
            # db.session.bind(self.u2)
            db.session.commit()

            resp = c.get(f'users/{self.u1.id}/following')

            html = resp.get_data(as_text=True)

            breakpoint()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser2', html)
