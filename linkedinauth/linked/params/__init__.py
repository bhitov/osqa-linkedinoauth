from functools import partial
from urllib import urlencode

class Fields(object):
    """
    Abstract class that shouldn't be initiated.
    Field classes should inherit this class and run _init_values in their __init__ method
    """
    
    def _init_values(self, simple_fields, complex_fields=None):
        if complex_fields is None: complex_fields = {} 
        self._values = dict()
         
        for key in simple_fields:
            self._values[key] = False
            method_key = "add_" + key.replace("-", "_")
            function = self._get_simple_lambda(key)
            function.__doc__ = "Add " + key
            function.__name__ = method_key
            setattr(self, method_key, function)
            
        for key, class_type in complex_fields.items():
            self._values[key] = False
            method_key = "add_" + key.replace("-", "_")
            function = self._get_complex_lambda(key, class_type)
            function.__doc__ = "Add " + key
            function.__name__ = method_key
            setattr(self, method_key, function)

    def _get_simple_lambda(self, key):
        return lambda: self._set_field(key)

    def _get_complex_lambda(self, key, class_type):
        return lambda value=None: self._set_complex_field(key, class_type, value)
    
    def __repr__(self):
        rep = []
        for key, value in self._values.items():
            if value is True:
                rep.append(key)
            elif isinstance(value, Fields):
                rep.append("{key}:({value})".format(key=key, value=repr(value)))
            elif value:
                rep.append(value)
        return self.__class__.__name__ + " : " + repr(rep)
            
    def _set_field(self, key):
        self._check_key_valid(key)
        
        self._values[key] = True
        return self
    
    def _check_key_valid(self, key):
        if not self._values.has_key(key):
            raise ValueError("{0} is not a valid field".format(key))
        
    def _set_complex_field(self, key, class_type, value=None):
        if not value:
            return self._set_field(key)
        
        self._check_key_valid(key)
        
        if not isinstance(value, class_type):
            raise ValueError("{0} is not of type {1}".format(value, class_type))
        
        self._values[key] = value
        return self
    
    def get_url(self):
        url_values = [key for key in self._values.keys() if self._values[key] is True]
        for key, value in self._values.items():
            if isinstance(value, Fields):
                url_values.append("{key}:({value})".format(key=key, value=value.get_url()))
            elif not isinstance(value, bool):
                url_values.append(value)
                
        return ",".join(url_values)
    
    def all(self):
        for key in self._values.keys():
            self._values[key] = True
        return self

class Location(Fields):
    def __init__(self):
        self._init_values(("name", "country"))
        
    def all_with_nested(self):
        return self.all()
    
class RelationToViewer(Fields):
    def __init__(self):
        self._init_values(("distance", "num-related-connections", "related-connections"))
        
    def all_with_nested(self):
        return self.all()
        
class MemberUrl(Fields):
    def __init__(self):
        self._init_values(("url", "name"))
        
    def all_with_nested(self):
        return self.all()
        
class HttpHeader(Fields):
    def __init__(self):
        self._init_values(("name", "value"))
        
    def all_with_nested(self):
        return self.all()
        
class HttpRequest(Fields):
    def __init__(self):
        self._init_values(("url",), {"headers" : HttpHeader})
        
    def all_with_nested(self):
        return self.add_url().add_headers(HttpHeader().all_with_nested())

class Company(Fields):
    def __init__(self):
        self._init_values(("id", "name", "type", "size", "industry", "ticker"))
        
    def all_with_nested(self):
        return self.all()

class Position(Fields):
    def __init__(self):
        self._init_values(("id", "title", "summary", "start-date",
                           "end-date", "is-current"),
                          {"company" : Company})
        
    def all_with_nested(self):
        return self.all().add_company(Company().all_with_nested())

class Author(Fields):
    def __init__(self):
        self._init_values(("id", "name", "person"))
        
    def all_with_nested(self):
        return self.all()

class Publication(Fields):
    def __init__(self):
        self._init_values(("id", "title", "publisher", "date", "url", "summary"),
                          {"authors" : Author})
        
    def all_with_nested(self):
        return self.all().add_author(Author().all_with_nested())

class PatentStatus(Fields):
    def __init__(self):
        self._init_values(("id", "name"))
        
    def all_with_nested(self):
        return self.all()
    
class Investor(Fields):
    def __init__(self):
        self._init_values(("id", "name"), {"person" : Profile})
        
    def all_with_nested(self):
        # We can't nest person because it will cause an infinite loop
        return self.all()
    
class Patent(Fields):
    def __init__(self):
        self._init_values(("id", "title", "summary", "number", "office", "date", "url"),
                          {"status" : PatentStatus,
                           "investors" : Investor})
        
    def all_with_nested(self):
        return self.all().add_status(PatentStatus().all_with_nested()). \
            add_investors(Investor().all_with_nested())
        
class Proficiency(Fields):
    def __init__(self):
        self._init_values(("level", "name"))
        
    def all_with_nested(self):
        return self.all()
        
class Language(Fields):
    def __init__(self):
        self._init_values(("id", "language"), {"proficiency" : Proficiency})
        
    def all_with_nested(self):
        return self.all().add_proficiency(Proficiency().all_with_nested())
    
class Year(Fields):
    def __init__(self):
        self._init_values(("id", "name"))
        
    def all_with_nested(self):
        return self.all()
    
class Skill(Fields):
    def __init__(self):
        self._init_values(("id", "skill"),
                          {"proficiency" : Proficiency,
                           "years" : Year})
        
    def all_with_nested(self):
        return self.all().add_proficiency(Proficiency().all_with_nested()). \
            add_years(Year().all_with_nested())

class Certification(Fields):
    def __init__(self):
        self._init_values(("id", "name", "authority", "number", "start-date", "end-date"))
    
    def all_with_nested(self):
        return self.all()
    
class Education(Fields):
    def __init__(self):
        self._init_values(("id", "school-name", "field-of-study", "start-date", "end-date",
                           "degree", "activities", "notes"))
    
    def all_with_nested(self):
        return self.all()
    
class Recommendation(Fields):
    def __init__(self):
        self._init_values(("id", "recommendation-type", "recommender"))
        
    def all_with_nested(self):
        return self.all()
  
class Profile(Fields):
    # TODO Dont forget about these params: https://developer.linkedin.com/thread/2286
    def __init__(self):
        simple_fields = ("id",
            "first-name",
            "last-name",
            "headline",
            "distance",
            "current-share",
            "connections",
            "num-connections",
            "num-connections-capped",
            "summary",
            "specialties",
            "proposal-comments",
            "associations",
            "honors",
            "interests",
            "patents",
            "num-recommenders",
            "phone-numbers",
            "im-accounts",
            "twitter-accounts",
            "date-of-birth",
            "main-address",
            "picture-url",
            "public-profile-url",
            "site-standard-profile-request",
            "api-public-profile-request",
            "site-public-profile-request",
            )
        complex_fields = {
            "location" : Location,
            "relation-to-viewer" : RelationToViewer,
            "member-url-resources" : MemberUrl,
            "api-standard-profile-request" : HttpRequest,
            "positions" : Position,
            "three-current-positions" : Position,
            "three-past-positions" : Position,
            "publications" : Publication,
            "languages" : Language,
            "skills" : Skill,
            "certifications" : Certification,
            "educations" : Education,
            "recommendations-received" : Recommendation}
        
        self._init_values(simple_fields, complex_fields)
        
        self._id = None
        self._url = None
        self._public = False
    
    def me(self):
        self._id = None
        self._url = None
        return self
        
    def set_url(self, url):
        self._id = None
        self._url = url
        return self
        
    def set_id(self, _id):
        self._url = None
        self._id = _id
        return self
    
    def public(self):
        self._public = True
        return self
    
    def private(self):
        self._public = False
        return self
    
    def all_with_nested(self):
        self.all()
        self._values["location"] = Location().all_with_nested()
        self._values["relation-to-viewer"] = RelationToViewer().all_with_nested()
        self._values["member-url-resources"] = MemberUrl().all_with_nested()
        self._values["api-standard-profile-request"] = HttpRequest.all_with_nested()
        return self
    
    def default(self):
        return self.add_first_name().add_last_name().add_headline() \
            .add_site_standard_profile_request()
        
    def get_url_for_api(self):
        url = ""
        if self._id:
            url = urlencode({"id" : self._id})
        elif self._url:
            url = urlencode({"url" : self._url})
        else:
            url = "~"
            
        if self._public:
            url += ":public"
        
        fields = self.get_url()
        if fields:
            url += ":(" + fields + ")"
        
        return url