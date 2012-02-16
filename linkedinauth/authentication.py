from consumer import OAuthAbstractAuthConsumer
from forum.authentication.base import ConsumerTemplateContext

try:
    import json as simplejson
except ImportError:
    from django.utils import simplejson

from lib import oauth
import settings

class LinkedinAuthConsumer(OAuthAbstractAuthConsumer):
    def __init__(self):
        OAuthAbstractAuthConsumer.__init__(self,
            str(settings.LINKEDIN_CONSUMER_KEY),
            str(settings.LINKEDIN_CONSUMER_SECRET),
            "https://api.linkedin.com", #maybe? find out what this parameter is
            "https://api.linkedin.com/uas/oauth/requestToken",
            "https://api.linkedin.com/uas/oauth/accessToken",
            "https://www.linkedin.com/uas/oauth/authorize",
        )

    def get_user_data(self, key):
        json = self.fetch_data(key, "http://api.linkedin.com/v1/people/~:(id)?format=json")
        #json = self.fetch_data(key, "https://twitter.com/account/verify_credentials.json")
        print "JSON DATA!!!"
        print json
        print "JSON DATA END!!!"

        if 'id' in json:
            creds = simplejson.loads(json)
            username = creds['id']
            return {
                'username': username
            }


        return {}

class LinkedinAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'DIRECT'
    weight = 150
    human_name = 'Linkedin'
    icon = '/media/images/openid/linkedin.png'
