from __future__ import annotations
from typing import TYPE_CHECKING, List
from flask import url_for

from mavis_reporting.models.organisation import Organisation

if TYPE_CHECKING:
    from mavis_reporting.models.region import Region
    from mavis_reporting.models.school import School


class Provider(Organisation):
    def __init__(self, provider: dict, region: Region = None):
        super().__init__(provider)
        self.schools: List[School] = []
        self.region: Region = region
        self.fake_measures("provider")

    def url(self) -> str:
        return url_for("main.provider", code=self.code)

    def school(self, code: str) -> School | None:
        for school in self.schools:
            if school.code == code:
                return school
        return None
