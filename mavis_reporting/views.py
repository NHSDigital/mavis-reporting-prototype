from functools import wraps
from flask import (
    Blueprint,
    render_template,
    g,
    redirect,
    url_for,
    abort,
    request,
    session,
)
import logging

from mavis_reporting.api.client import MavisAPI
from mavis_reporting.helpers.breacrumb_helper import generate_breadcrumb_items
from mavis_reporting.helpers.secondary_nav_helper import generate_secondary_nav_items

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
    g.measures = api.measures()


@main.context_processor
def inject_mavis_data():
    """Inject Mavis variables used to filter data into the template context."""
    return {
        "programmes": g.programmes,
        "year_groups": g.year_groups,
        "genders": g.genders,
        "site_title": "Manage vaccinations in schools",
    }


def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user", None):
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("role")
        return redirect(url_for("main.index"))

    return render_template("login.jinja", region=g.region)


@main.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.login"))


@main.route("/")
@session_required
def index():
    if session["user"] == "region":
        return redirect(url_for("main.region", code=g.region.code))
    elif session["user"] == "provider":
        return redirect(url_for("main.provider", code=g.region.providers[0].code))
    else:
        abort(404)


@main.route("/region/<code>")
@session_required
def region(code):
    if session["user"] != "region":
        abort(404)

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
@session_required
def region_providers(code):
    if session["user"] != "region":
        abort(404)

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
@session_required
def provider(code):
    provider = g.region.provider(code)
    if not provider:
        abort(404)

    breadcrumb_items = [provider]
    if session["user"] == "region":
        breadcrumb_items.insert(0, g.region)

    return render_template(
        "organisation.jinja",
        title=provider.name,
        org_type_title="Provider",
        organisation=provider,
        breadcrumb_items=generate_breadcrumb_items(breadcrumb_items),
        secondary_navigation_items=generate_secondary_nav_items(
            "provider", code, "provider"
        ),
    )


@main.route("/providers/<code>/schools")
@session_required
def provider_schools(code):
    provider = g.region.provider(code)
    if not provider:
        abort(404)

    breadcrumb_items = [provider]
    if session["user"] == "region":
        breadcrumb_items.insert(0, g.region)

    return render_template(
        "organisation_children.jinja",
        title=f"Schools - {provider.name}",
        org_type_title="Provider",
        child_type_title_singular="School",
        child_type_title_plural="Schools",
        organisation=provider,
        children=provider.schools,
        breadcrumb_items=generate_breadcrumb_items(breadcrumb_items),
        secondary_navigation_items=generate_secondary_nav_items(
            "provider", code, "provider_schools"
        ),
    )


@main.route("/schools/<code>")
@session_required
def school(code):
    school = g.region.school(code)
    if not school:
        abort(404)

    breadcrumb_items = [school.provider, school]
    if session["user"] == "region":
        breadcrumb_items.insert(0, g.region)

    return render_template(
        "organisation.jinja",
        title=school.name,
        org_type_title="School",
        organisation=school,
        breadcrumb_items=generate_breadcrumb_items(breadcrumb_items),
        secondary_navigation_items=generate_secondary_nav_items(
            "school", code, "school"
        ),
    )


@main.route("/data-definitions")
@session_required
def data_definitions():
    return render_template("data_definitions.jinja")


@main.route("/download", methods=["GET", "POST"])
@session_required
def download():
    if request.method == "POST":
        return redirect(url_for("main.download"))

    measures = [
        {
            "text": measure["name"],
            "description": measure["description"],
            "value": measure["code"],
            "hint": {
                "text": measure["description"],
            },
        }
        for measure in g.measures.values()
    ]

    return render_template(
        "download.jinja",
        programmes=g.programmes,
        providers=g.region.providers,
        measures=measures,
    )


@main.errorhandler(404)
def page_not_found():
    return render_template("errors/404.html"), 404
