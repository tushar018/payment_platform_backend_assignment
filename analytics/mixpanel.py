# mixpanel_utils.py
from mixpanel import Mixpanel
from django.conf import settings


class MixpanelClient:
    def __init__(self):
        self.mixpanel = Mixpanel(settings.MIXPANEL_TOKEN)

    def track_event(self, event_name, properties=None):
        self.mixpanel.track(event_name=event_name, properties=properties or {}, distinct_id='TEMP')

    def identify_user(self, user_id):
        self.mixpanel.identify(user_id)


mixpanel_client = MixpanelClient()
