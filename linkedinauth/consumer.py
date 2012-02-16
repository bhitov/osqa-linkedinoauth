import urllib
import urllib2
import httplib
import time

from forum.authentication.base import AuthenticationConsumer, InvalidAuthentication
from django.utils.translation import ugettext as _
from django.utils import simplejson as json

from lib import oauth
import oauth2
import settings
from linked import linkedin

class OAuthAbstractAuthConsumer(AuthenticationConsumer):

    def __init__(self, consumer_key, consumer_secret, server_url, request_token_url, access_token_url, authorization_url):
        self.consumer_secret = consumer_secret
        self.consumer_key = consumer_key

        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

        self.server_url = server_url
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url

    def prepare_authentication_request(self, request, redirect_to):
        request_token = self.fetch_request_token()
        request.session['unauthed_token'] = request_token.to_string()
        return self.authorize_token_url(request_token)

    def process_authentication_request(self, request):
        unauthed_t = request.session.get('unauthed_token')
        bleh = unauthed_t.replace('&','=').split('=')
        oauth_token = bleh[3]
        oauth_secret = bleh[1]

        oauth_verifier = request.GET['oauth_verifier']

        api = linkedin.LinkedIn(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET, "http://careervillage.org")
        errors = True

        try:
            api.access_token(oauth_token, oauth_secret, oauth_verifier)
            errors = False
        except:
            pass

        if not errors:
            a_tok = oauth.OAuthToken(api._access_token, api._access_token_secret)
            blerp = a_tok.to_string()
            return blerp
        return


    def get_user_data(self, key):
        #token = oauth.OAuthToken.from_string(access_token)
        return {}

    def fetch_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_url=self.request_token_url)

        oauth_request.sign_request(self.signature_method, self.consumer, None)
        params = oauth_request.parameters
        data = urllib.urlencode(params)

        full_url='%s?%s'%(self.request_token_url, data)
        response = urllib2.urlopen(full_url)

        return oauth.OAuthToken.from_string(response.read())

    def authorize_token_url(self, token, callback_url=None):
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token,\
            callback=callback_url, http_url=self.authorization_url)
        params = oauth_request.parameters
        data = urllib.urlencode(params)
        full_url='%s?%s'%(self.authorization_url, data)
        return full_url

    def fetch_access_token(self, token):
        print "hey"
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_url=self.access_token_url)
        oauth_request.sign_request(self.signature_method, self.consumer, token)
        print "hey3"

        params = oauth_request.parameters
        params['oauth_verifier'] = '19163'
        data = urllib.urlencode(params)
        full_url='%s?%s'%(self.access_token_url, data)
        print "hey5"

        print "url: ", self.access_token_url
        print "data: ", params
        request = urllib2.Request(self.access_token_url, data)
        response = urllib2.urlopen(request)
        #        response = urllib2.urlopen(full_url)

        print "hey6"
        return oauth.OAuthToken.from_string(response.read())

    def fetch_data(self, token, http_url, parameters=None):
        access_token = oauth.OAuthToken.from_string(token)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer, token=access_token, http_method="GET",
            http_url=http_url, parameters=parameters,
        )
        oauth_request.sign_request(self.signature_method, self.consumer, access_token)

        url = oauth_request.to_url()
        connection = httplib.HTTPSConnection(self.server_url)
        connection.request(oauth_request.http_method, url)

        return connection.getresponse().read()

