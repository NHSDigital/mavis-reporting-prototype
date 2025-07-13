from flask import Blueprint, render_template, g, redirect, url_for
import logging

from mavis_reporting.api.client import MavisAPI

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.before_request
def get_region():
    """Get core data from the API and store it in the global g object."""
    api = MavisAPI()
    g.region = api.region()
    g.programmes = api.programmes()
    g.year_groups = api.year_groups()
    g.genders = api.genders()


@main.context_processor
def inject_mavis_data():
    """Inject Mavis variables used to filter data into the template context."""
    return {
        "programmes": g.programmes,
        "year_groups": g.year_groups,
        "genders": g.genders,
    }


@main.route("/")
def index():
    return redirect(url_for("main.region", code=g.region.code))


@main.route("/region/<code>")
def region(code):
    if code != g.region.code:
        return redirect(url_for("main.region", code=g.region.code))

    secondary_navigation_items = [
        {
            "text": "Overview",
            "current": True,
            "href": url_for("main.region", code=g.region.code),
        },
        {
            "text": "Providers",
            "current": False,
            "href": url_for("main.region_providers", code=g.region.code),
        },
    ]

    return render_template(
        "organisation.jinja",
        page="region",
        title=g.region.name,
        org_type_title="Region",
        organisation=g.region,
        secondary_navigation_items=secondary_navigation_items,
    )


@main.route("/region/<code>/providers")
def region_providers(code):
    if code != g.region.code:
        return redirect(url_for("main.region_providers", code=g.region.code))

    secondary_navigation_items = [
        {
            "text": "Overview",
            "current": False,
            "href": url_for("main.region", code=g.region.code),
        },
        {
            "text": "Providers",
            "current": True,
            "href": url_for("main.region_providers", code=g.region.code),
        },
    ]

    return render_template(
        "region_providers.jinja",
        page="providers",
        title=g.region.name,
        org_type_title="Region",
        region=g.region,
        providers=g.region.providers,
        secondary_navigation_items=secondary_navigation_items,
    )


@main.route("/providers/<provider_code>")
def provider(provider_code):
    provider = g.region.provider(provider_code)
    if not provider:
        return "Provider not found", 404

    secondary_navigation_items = [
        {
            "text": "Overview",
            "current": True,
            "href": url_for("main.provider", provider_code=provider_code),
        },
        {"text": "Schools", "current": False, "href": "#"},
    ]

    return render_template(
        "organisation.jinja",
        page="provider",
        title=provider.name,
        org_type_title="Provider",
        organisation=provider,
        secondary_navigation_items=secondary_navigation_items,
    )
