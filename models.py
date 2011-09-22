
from google.appengine.ext import db

class Tweet(db.Model):

    message_id = db.IntegerProperty(required=True)
    message = db.TextProperty(required=True)
    user_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    profile_image_url = db.LinkProperty()
    created_at = db.DateTimeProperty()
    added_at = db.DateTimeProperty(auto_now_add=True)
    location = db.GeoPtProperty()

    def url(self):
        return "http://twitter.com/%s/status/%d" % (
            self.username, self.message_id) 


class KeyStore(db.Model):
    name = db.StringProperty(required=True)
    value = db.StringProperty()
