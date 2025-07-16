from __future__ import annotations
from typing import TYPE_CHECKING
from flask import url_for

from mavis_reporting.models.organisation import Organisation

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider
    from mavis_reporting.models.school import School


class Region(Organisation):
    def __init__(self, region: dict):
        super().__init__(region)
        self.providers: list[Provider] = []
        self.schools: list[School] = []
        self.type = "region"
        self.fake_measures(self.type)

    def url(self) -> str:
        return url_for("main.region", code=self.code)

    def provider(self, provider_value: str) -> Provider | None:
        for provider in self.providers:
            if provider.code == provider_value:
                return provider
        return None

    def school(self, code: str) -> School | None:
        for school in self.schools:
            if school.code == code:
                return school
        return None
