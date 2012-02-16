from forum.settings import EXT_KEYS_SET
from forum.settings.base import Setting

LINKEDIN_CONSUMER_KEY = Setting('LINKEDIN_CONSUMER_KEY', '', EXT_KEYS_SET, dict(
    label = "LinkedIn consumer key",
    help_text = """
hint: it's what the label says it is
""",
    required=False))

LINKEDIN_CONSUMER_SECRET = Setting('LINKEDIN_CONSUMER_SECRET', '', EXT_KEYS_SET, dict(
    label = "LinkedIn consumer secret",
    help_text = """
Puppies are awesome
""",
    required=False))
