
from app.models import Comment,User,Pitch
from app import db
import unittest
Pitch = Pitch
class CommentTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Pitch class
    '''
    def setUp(self):
        self.user_dema = User(username = 'dema',password = 'okay', email = 'dema@dema.com')
        self.new_pitch = Pitch('Hello world','My first webpage','Projects')
        self.new_comment = Comment(pitch_id=1,comment='Awesome',user = self.user_dema ) 

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.pitch_id,1)
        self.assertEquals(self.new_comment.comment,'Awesome')
        self.assertEquals(self.new_comment.user,self.user_dema) 

    def test_save_comment(self): 
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments(15)
        self.assertTrue(len(got_comments) == 1)