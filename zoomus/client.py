"""Zoom.us REST API Python Client"""

from __future__ import absolute_import, unicode_literals

from zoomus import components, util
from zoomus.util import API_VERSION_1, API_VERSION_2


API_BASE_URIS = {
    API_VERSION_1: "https://api.zoom.us/v1",
    API_VERSION_2: "https://api.zoom.us/v2",
}

COMPONENT_CLASSES = {
    API_VERSION_1: {
        "user": components.user.UserComponent,
        "group": components.group.GroupComponent,
        "meeting": components.meeting.MeetingComponent,
        "report": components.report.ReportComponent,
        "webinar": components.webinar.WebinarComponent,
        "recording": components.recording.RecordingComponent,
    },
    API_VERSION_2: {
        "user": components.user.UserComponentV2,
        "group": components.group.GroupComponentV2,
        "meeting": components.meeting.MeetingComponentV2,
        "metric": components.metric.MetricComponentV2,
        "past_meeting": components.past_meeting.PastMeetingComponentV2,
        "report": components.report.ReportComponentV2,
        "webinar": components.webinar.WebinarComponentV2,
        "recording": components.recording.RecordingComponentV2,
        "phone": components.phone.PhoneComponentV2,
    },
}


class ZoomClient(util.ApiClient):
    """Zoom.us REST API Python Client"""

    """Base URL for Zoom API"""

    def __init__(
        self,
        key,
        secret_or_url,
        gravitee=False,
        data_type="json",
        timeout=15,
        version=API_VERSION_2,
    ):
        """Create a new Zoom client

        Supports gravitee while being API compatible with old usage.
        api_key and api_secret.

        :param key: The API key, either for Zoom.us or for Gravitee
        :param secret_or_url: Either the Zoom.us API secret or the Gravitee URL
        :param gravitee: Are we to use Gravitee?
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        """
        try:
            BASE_URI = API_BASE_URIS[version]
            self.components = COMPONENT_CLASSES[version].copy()
        except KeyError:
            raise RuntimeError("API version not supported: %s" % version)

        if gravitee:
            BASE_URI = secret_or_url

        super(ZoomClient, self).__init__(base_uri=BASE_URI, timeout=timeout)

        if gravitee:
            self.config = {
                "gravitee_key": key,
                "data_type": data_type,
                "version": version,
            }
        else:
            self.config = {
                "api_key": key,
                "api_secret": secret_or_url,
                "data_type": data_type,
                "version": version,
                "token": util.generate_jwt(key, secret_or_url),
            }

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                base_uri=BASE_URI, config=self.config
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def refresh_token(self):
        self.config["token"] = (
            util.generate_jwt(self.config["api_key"], self.config["api_secret"]),
        )

    @property
    def api_key(self):
        """The Zoom.us api_key"""
        return self.config.get("api_key")

    @api_key.setter
    def api_key(self, value):
        """Set the api_key"""
        self.config["api_key"] = value
        self.refresh_token()

    @property
    def api_secret(self):
        """The Zoom.us api_secret"""
        return self.config.get("api_secret")

    @api_secret.setter
    def api_secret(self, value):
        """Set the api_secret"""
        self.config["api_secret"] = value
        self.refresh_token()

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get("meeting")

    @property
    def metric(self):
        """Get the metric component"""
        return self.components.get("metric")

    @property
    def report(self):
        """Get the report component"""
        return self.components.get("report")

    @property
    def user(self):
        """Get the user component"""
        return self.components.get("user")

    @property
    def group(self):
        """Get the group component"""
        return self.components.get("group")

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get("webinar")

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get("recording")

    @property
    def phone(self):
        """Get the phone component"""
        return self.components.get("phone")

class ZoomGraviteeClient(ZoomClient):
    """Zoom.us REST API Python Client over Gravitee"""

    def __init__(
        self, gravitee_api_key, url, data_type="json", timeout=15, version=API_VERSION_2
    ):

        super(ZoomGraviteeClient, self).__init__(gravitee_api_key, url, gravitee=True, data_type=data_type, timeout=timeout, version=version)