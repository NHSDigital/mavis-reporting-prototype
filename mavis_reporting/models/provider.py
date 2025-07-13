from __future__ import annotations

from typing import TYPE_CHECKING, List

from mavis_reporting.helpers.measure_faker_helper import MeasureFaker

if TYPE_CHECKING:
    from mavis_reporting.models.region import Region
    from mavis_reporting.models.school import School


class Provider:
    def __init__(self, provider: dict, region: Region = None):
        self.name: str = provider["name"]
        self.value: str = provider["value"]
        self.schools: List[School] = []
        self.region: Region = region
        self.fake_measures()

    def fake_measures(self) -> None:
        faker = MeasureFaker(self.name)
        self._fake_cohort_size: int = faker.eligible_cohort_size("provider")
        self._measures: dict[str, int] = faker.measures(self._fake_cohort_size)

    def school(self, school_value: str) -> School | None:
        for school in self.schools:
            if school.value == school_value:
                return school
        return None

    def measure_value(self, measure: str) -> int | None:
        if measure == "eligible_cohort":
            return self._fake_cohort_size

        if measure in self._measures:
            return self._measures[measure]
        return None
