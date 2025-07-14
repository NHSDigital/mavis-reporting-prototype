from __future__ import annotations
from typing import TYPE_CHECKING
from flask import url_for

from mavis_reporting.models.organisation import Organisation

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider
    from mavis_reporting.models.region import Region


class School(Organisation):
    def __init__(self, school: dict, provider: Provider, region: Region = None):
        super().__init__(school)
        self.code: str = school["code"]
        self.provider: Provider = provider
        self.region: Region = region
        self.fake_measures("school")

    def url(self) -> str:
        return url_for("main.school", code=self.code)
