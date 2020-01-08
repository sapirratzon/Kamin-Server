from Entities.comment import Comment
from kamin_API import app
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # Comment("ron", "lalalalal", "", 1).serialize()),
    # test code

    def test_get_discussion(self):
        with app.app_context():
            response = app.test_client().post(
                '/getDiscussion/1',
                data=Comment("ron", "lalalalal", None, 0),
                content_type='application/json',
            )
            data = response.get_data()
            print(data)

    def test_add_comment(self):
        with app.app_context():
            response = app.test_client().post(
                '/addComment',
                data=Comment("ron", "lalalalal", None, 0),
                # {"comment": {"user_name": "ron", "content": "lalalalal", "commented_to": "", "discussion_id": 1}}),
                content_type='application/json',
            )
            data = response.get_data()
            print(data)

            assert data is None


test = MyTestCase()
test.test_add_comment()
