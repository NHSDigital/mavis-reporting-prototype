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
import urllib.parse, urllib.request

from mavis_reporting.helpers import mavis_helper
from mavis_reporting.helpers import auth_helper
from mavis_reporting.helpers import url_helper

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
@auth_helper.login_required
def index():
    return render_template("index.jinja")


@main.route("/api-call")
@auth_helper.login_required
def api_call():
    response = mavis_helper.api_call(current_app, session, "/reporting/totals")
    data = response.json()
    return render_template("api_call.jinja", response=response, data=data)
