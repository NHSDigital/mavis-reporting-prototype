from __future__ import annotations
from typing import TYPE_CHECKING

from mavis_reporting.helpers.measure_faker_helper import MeasureFaker

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider


class Region:
    def __init__(self, region: dict):
        self.name: str = region["name"]
        self.value: str = region["value"]
        self.providers: list[Provider] = []
        self.fake_measures()

    def fake_measures(self) -> None:
        faker = MeasureFaker(self.name)
        self._fake_cohort_size: int = faker.eligible_cohort_size("region")
        self._measures: dict[str, int] = faker.measures(self._fake_cohort_size)

    def provider(self, provider_value: str) -> Provider | None:
        for provider in self.providers:
            if provider.value == provider_value:
                return provider
        return None

    def measure_value(self, measure: str) -> int | None:
        if measure == "eligible_cohort":
            return self._fake_cohort_size

        if measure in self._measures:
            return self._measures[measure]
        return None
