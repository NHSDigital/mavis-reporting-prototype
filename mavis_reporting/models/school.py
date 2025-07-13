from __future__ import annotations
from typing import TYPE_CHECKING

from flask import url_for

from mavis_reporting.helpers.measure_faker_helper import MeasureFaker

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider


class School:
    def __init__(self, school: dict, provider: Provider = None):
        self.name: str = school["name"]
        self.urn: str = school["urn"]
        self.provider: Provider = provider
        self.fake_measures()

    def fake_measures(self) -> None:
        faker = MeasureFaker(self.name)
        self._fake_cohort_size: int = faker.eligible_cohort_size("school")
        self._measures: dict[str, int] = faker.measures(self._fake_cohort_size)

    def url(self) -> str:
        return url_for("main.school", urn=self.urn)

    def measure_value(self, measure: str) -> int | None:
        if measure == "eligible_cohort":
            return self._fake_cohort_size

        if measure in self._measures:
            return self._measures[measure]
        return None
