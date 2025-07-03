from datetime import datetime, timezone
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
)

import json
import logging
import requests
import urllib.parse, urllib.request

from mavis_reporting.api.client import MavisAPI
from mavis_reporting.helpers.breacrumb_helper import generate_breadcrumb_items
from mavis_reporting.helpers.secondary_nav_helper import generate_secondary_nav_items

from mavis_reporting.helpers import mavis_helper
from mavis_reporting.helpers import auth_helper

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


def session_expired():
    last_visit = session.get("last_visit")
    if last_visit is None:
        return True

    session_age = (datetime.now().astimezone(timezone.utc) - last_visit).total_seconds()
    return abs(session_age) > current_app.config["SESSION_TTL_SECONDS"]


def is_logged_in():
    if "user_id" in session:
        if session_expired():
            session.clear()
            return False
        else:
            return True

    else:
        return False


def mavis_url(path):
    return current_app.config["MAVIS_ROOT_URL"] + path


def verify_token(token):
    url = mavis_url("/tokens/" + token)
    user_data = None

    headers = {"Authorization": current_app.config["SECRET_KEY"]}
    r = requests.get(url, headers=headers)
    logger.info("response from verify_token call", r.status_code)
    logger.info("response body ", r.text)

    user_data = r.json()

    return user_data


def log_user_in(data):
    session["user_id"] = data["user_id"]
    session["created_at"] = data["created_at"]
    session["last_visit"] = datetime.now()
    session["cis2_info"] = data["cis2_info"]
    session["user"] = data["user"]


@main.before_request
def get_region():
    """Get core data from the API and store it in the global g object."""
    api = MavisAPI()
    g.region = api.region()
    logger.warning(api.programmes())
    g.programmes = [
        {
            "value": programme["code"],
            "text": programme["text"],
            "checked": True if programme["code"] == "hpv" else False,
        }
        for programme in api.programmes()
    ]
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
@login_required
def index():
    return redirect(url_for("main.region", code=g.region.code))


@main.route("/region/<code>")
def region(code):
    if code != g.region.code:
        return redirect(url_for("main.region", code=g.region.code))

    return render_template(
        "organisation.jinja",
        title=g.region.name,
        org_type_title="Region",
        organisation=g.region,
        breadcrumb_items=generate_breadcrumb_items([g.region]),
        secondary_navigation_items=generate_secondary_nav_items(
            "region", g.region.code, "region"
        ),
    )


@main.route("/region/<code>/providers")
def region_providers(code):
    if code != g.region.code:
        abort(404)

    return render_template(
        "organisation_children.jinja",
        title=f"Providers - {g.region.name}",
        org_type_title="Region",
        child_type_title_singular="Provider",
        child_type_title_plural="Providers",
        organisation=g.region,
        children=g.region.providers,
        breadcrumb_items=generate_breadcrumb_items([g.region]),
        secondary_navigation_items=generate_secondary_nav_items(
            "region", g.region.code, "region_providers"
        ),
    )


@main.route("/providers/<code>")
def provider(code):
    provider = g.region.provider(code)
    if not provider:
        abort(404)

    return render_template(
        "organisation.jinja",
        title=provider.name,
        org_type_title="Provider",
        organisation=provider,
        breadcrumb_items=generate_breadcrumb_items([g.region, provider]),
        secondary_navigation_items=generate_secondary_nav_items(
            "provider", code, "provider"
        ),
    )


@main.route("/providers/<code>/schools")
def provider_schools(code):
    provider = g.region.provider(code)
    if not provider:
        abort(404)

    return render_template(
        "organisation_children.jinja",
        title=f"Schools - {provider.name}",
        org_type_title="Provider",
        child_type_title_singular="School",
        child_type_title_plural="Schools",
        organisation=provider,
        children=provider.schools,
        breadcrumb_items=generate_breadcrumb_items([g.region, provider]),
        secondary_navigation_items=generate_secondary_nav_items(
            "provider", code, "provider_schools"
        ),
    )


@main.route("/schools/<code>")
def school(code):
    school = g.region.school(code)
    if not school:
        abort(404)

    return render_template(
        "organisation.jinja",
        title=school.name,
        org_type_title="School",
        organisation=school,
        breadcrumb_items=generate_breadcrumb_items([g.region, school.provider, school]),
        secondary_navigation_items=generate_secondary_nav_items(
            "school", code, "school"
        ),
    )


@main.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@main.route("/healthcheck")
def healthcheck():
    return HealthCheck().run()
