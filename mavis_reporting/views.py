from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    current_app,
    url_for,
    g,
    abort,
)

from healthcheck import HealthCheck

from werkzeug.exceptions import Unauthorized

import logging

from mavis_reporting.api.client import MavisAPI
from mavis_reporting.helpers.breacrumb_helper import generate_breadcrumb_items
from mavis_reporting.helpers.secondary_nav_helper import generate_secondary_nav_items

from mavis_reporting.helpers import mavis_helper
from mavis_reporting.helpers import auth_helper
from mavis_reporting.helpers import url_helper

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
def root():
    return redirect(url_helper.prepend_path(request.full_path, "/reporting"))


@main.route("/reporting/")
@auth_helper.login_required
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
    return render_template("index.jinja")


@main.route("/reporting/api-call/")
@auth_helper.login_required
def api_call():
    response = None
    try:
        response = mavis_helper.api_call(current_app, session, "/reporting-api/totals")
    except Unauthorized:
        return mavis_helper.login_and_return_after(current_app, request.url)

    data = response.json()
    return render_template("api_call.jinja", response=response, data=data)
