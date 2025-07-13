from flask import Blueprint, render_template, g, redirect, url_for
import logging

from mavis_reporting.api.client import MavisAPI

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.before_request
def get_region():
    """Get the region data from the API and store it in the g object."""
    api = MavisAPI()
    g.region = api.region()
    g.programmes = api.programmes()
    g.year_groups = api.year_groups()
    g.genders = api.genders()


@main.route("/")
def index():
    return redirect(url_for("main.region", code=g.region.code))


@main.route("/region/<code>")
def region(code):
    if code != g.region.code:
        return redirect(url_for("main.region", code=g.region.code))

    return render_template(
        "region.jinja",
        page="region",
        title=g.region.name,
        region=g.region,
        programmes=g.programmes,
        year_groups=g.year_groups,
        genders=g.genders,
    )


@main.route("/region/<code>/providers")
def providers(code):
    if code != g.region.code:
        return redirect(url_for("main.providers", code=g.region.code))

    return render_template(
        "providers.jinja",
        page="providers",
        title=g.region.name,
        region=g.region,
        providers=g.region.providers,
        programmes=g.programmes,
        year_groups=g.year_groups,
        genders=g.genders,
    )
