from mavis_reporting.api.data.gender import genders
from mavis_reporting.api.data.programme import programmes
from mavis_reporting.api.data.region import midlands
from mavis_reporting.api.data.measures import measures
from mavis_reporting.api.data.year_group import year_groups
from mavis_reporting.helpers.region_data_helper import process_region_data
from mavis_reporting.models.region import Region


class MavisAPI:
    def __init__(self):
        self._region: Region = None

    def region(self) -> Region:
        if self._region is None:
            self._region = process_region_data(midlands)
        return self._region

    def genders(self) -> list[dict]:
        return genders

    def programmes(self) -> list[dict]:
        return programmes

    def year_groups(self) -> list[dict]:
        return year_groups

    def measures(self) -> dict[str, dict]:
        return measures
