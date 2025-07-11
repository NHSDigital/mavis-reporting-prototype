from flask import Blueprint, render_template
import logging

from mavis_reporting.config.mavis import programmes, year_groups, genders

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template(
        "index.jinja",
        page="region",
        programmes=programmes,
        year_groups=year_groups,
        genders=genders,
    )


@main.route("/providers")
def providers():
    return render_template(
        "providers.jinja",
        page="providers",
        programmes=programmes,
        year_groups=year_groups,
        genders=genders,
    )
