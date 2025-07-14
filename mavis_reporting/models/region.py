from __future__ import annotations
from typing import TYPE_CHECKING

from flask import url_for

from mavis_reporting.helpers.measure_faker_helper import MeasureFaker

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider
    from mavis_reporting.models.school import School


class Region:
    def __init__(self, region: dict):
        self.name: str = region["name"]
        self.code: str = region["code"]
        self.providers: list[Provider] = []
        self.schools: list[School] = []
        self.fake_measures()

    def fake_measures(self) -> None:
        faker = MeasureFaker(self.name)
        self._fake_cohort_size: int = faker.eligible_cohort_size("region")
        self._measures: dict[str, int] = faker.measures(self._fake_cohort_size)

    def url(self) -> str:
        return url_for("main.region", code=self.code)

    def provider(self, provider_value: str) -> Provider | None:
        for provider in self.providers:
            if provider.code == provider_value:
                return provider
        return None

    def school(self, urn: str) -> School | None:
        for school in self.schools:
            if school.urn == urn:
                return school
        return None

    def measure_value(self, measure: str) -> int | None:
        if measure == "eligible_cohort":
            return self._fake_cohort_size

        if measure in self._measures:
            return self._measures[measure]
        return None
