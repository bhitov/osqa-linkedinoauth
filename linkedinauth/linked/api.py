from linkedin import LinkedIn as OldLinkedIn
from params import *

class ConfigurationError(Exception):
    def __init__(self, error):
        self._error = error
        
    def __str__(self):
        return repr(self._error)
    
class LinkedIn(object):
    
    def __init__(self):
        self._linkedin = OldLinkedIn(None, None, None, False)
    
    def api_key(self, api_key):
        self._linkedin._api_key = api_key
        return self
        
    def secret_key(self, api_secret):
        self._linkedin._api_secret = api_secret
        return self
        
    def callback_url(self, callback_url):
        self._linkedin._callback_url = callback_url
        return self
    
    def gae(self):
        self._linkedin._gae = True
        return self
        
    def nogae(self):
        self._linkedin._gae = False
        return self
        
    def reset(self):
        self._linkedin.clear()
        return self
    

    def _check_basic_parameters(self):
        if not self._linkedin._api_key:
            raise ConfigurationError("Please run api_key() first")
        if not self._linkedin._api_secret:
            raise ConfigurationError("Please run secret_key() first")
        if not self._linkedin._callback_url:
            raise ConfigurationError("Please run callback_url() first")

    def request_token(self):
        self._check_basic_parameters()
        
        if self._linkedin._request_token or self._linkedin._access_token or \
            self._linkedin._verifier or self._linkedin._request_token_secret or \
            self._linkedin._access_token_secret:
            raise ConfigurationError("Please run reset() before running request_token again")
        
        self._linkedin.request_token()
        return self
    
    def get_authorize_url(self):
        if not (self._linkedin._request_token):
            raise ConfigurationError("Please run request_token() before running get_authorize_url()")
        return self._linkedin.get_authorize_url()
        
    def verifier(self, verifier):
        self._linkedin._verifier = verifier
        return self
    
    def access_token(self):
        if not (self._linkedin._request_token and self._linkedin._request_token_secret):
            raise ConfigurationError("Please run request_token() before running access_token()")
        
        if not self._linkedin._verifier:
            raise ConfigurationError("Please run verifier() before running access_token()")
        
        if self._linkedin._access_token or self._linkedin._access_token_secret:
            raise ConfigurationError("Please run reset() before running access_token again")
        
        self._linkedin.access_token()
        return self
        
    def profile(self, params = None):
        if not params:
            params = Profile()
        
        if isinstance(params, Profile):
            url = params.get_url_for_api()
        elif isinstance(params, str):
            url = params
        else:
            raise ValueError("Can't handle type {0}".format(params))
        
        return self._linkedin.get_profile_raw(url)
    