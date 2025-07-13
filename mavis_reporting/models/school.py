from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mavis_reporting.models.provider import Provider


class School:
    def __init__(self, school: dict, provider: Provider = None):
        self.name: str = school["name"]
        self.urn: str = school["urn"]
        self.provider: Provider = provider
