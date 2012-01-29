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
            "https://api.linkedin.com", 
            "https://api.linkedin.com/uas/oauth/requestToken",
            "https://api.linkedin.com/uas/oauth/accessToken",
            "https://www.linkedin.com/uas/oauth/authorize",
        )

    def get_user_data(self, key):
        json = self.fetch_data(key, "http://api.linkedin.com/v1/people/~:(first-name,last-name)?format=json")

        if 'firstName' in json and 'lastName' in json:
            creds = simplejson.loads(json)
            username = creds['firstName'] + creds['lastName']
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
