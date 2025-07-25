# Ignoring line length for this file given it's faked data
# ruff: noqa: E501

from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from mavis_reporting.models.measure import Measure


provider_measures: List[Measure] = [
    {
        "text": "Sessions completed",
        "description": "Number of sessions completed",
        "value": "sessions_completed",
    },
    {
        "text": "Vaccinations",
        "description": "Number of vaccinations administered",
        "value": "vaccinations",
    },
]

child_measures: List[Measure] = [
    {
        "text": "Eligible cohort",
        "description": "Number of children eligible for the vaccine in this programme year",
        "value": "eligible_cohort",
    },
    {
        "text": "Consent offered",
        "description": "Number of children offered asked to consent",
        "value": "offered",
    },
    {
        "text": "Consent given",
        "description": "Number of children who have valid consent to receive the vaccine",
        "value": "consent_given",
    },
    {
        "text": "Consent refused",
        "description": "Number of children for whom consent was refused",
        "value": "refused",
    },
    {
        "text": "No response",
        "description": "Number of children for whom no response was received",
        "value": "no_response",
    },
    {
        "text": "Outstanding",
        "description": "Number of children with consent who have not yet received the vaccine",
        "value": "outstanding",
    },
    {
        "text": "Vaccinated",
        "description": "Number of children who have received the vaccine",
        "value": "vaccinated",
    },
]
