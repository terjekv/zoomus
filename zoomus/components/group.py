"""Zoom.us REST API Python Client -- Group component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class GroupComponent(base.BaseComponent):
    """Component dealing with all group related matters"""

    def list(self, **kwargs):
        return self.post_request("/group/list", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/group/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/groups/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/groups/delete", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/groups/get", params=kwargs)

class GroupComponentV2(base.BaseComponent):
    def list(self, **kwargs):
        return self.get_request("/groups", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/groups", data=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request("/groups/{}".format(kwargs.get("id")), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request("/groups/{}".format(kwargs.get("id")), params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/groups/{}".format(kwargs.get("id")), params=kwargs)

    def get_settings(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/groups/{}/settings".format(kwargs.get("id")), params=kwargs)

    def update_settings(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request("/groups/{}/settings".format(kwargs.get("id")), data=kwargs)

    def list_members(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/groups/{}/members".format(kwargs.get("id")), params=kwargs)

    def add_members(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request("/groups/{}/members".format(kwargs.get("id")), data=kwargs)

    def delete_member(self, **kwargs):
        util.require_keys(kwargs, ["id", "userid"])
        return self.delete_request("/groups/{}/members/{}".format(kwargs.get("id"),
                                   kwargs.get("userid")), data=kwargs)
