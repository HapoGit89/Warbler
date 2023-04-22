"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def test_message_model(self):
        """Does message model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text = "This is a test message",
            user_id = u.id
        )

        db.session.add(m)
        db.session.commit()

        #testing __repr__ func
        self.assertEqual(f"<Message #{m.id}: Text: {m.text}, Time: {m.timestamp}, User: {m.user_id}>", str(Message.query.filter_by(id=m.id).one()))
        # test if message shows up in user messages
        self.assertIn(m, u.messages)
        # test if user details can be accessed via message table
        self.assertEqual(u.username, m.user.username)

