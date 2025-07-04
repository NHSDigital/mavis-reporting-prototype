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
from functools import wraps

import json
import logging
import urllib.parse, urllib.request

from mavis_reporting.helpers import mavis_helper
from mavis_reporting.helpers import auth_helper

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if auth_helper.fake_login_enabled(current_app):
            logger.warning("FAKE_LOGIN_ENABLED! Logging in as fake_user_session_info")
            auth_helper.log_user_in(auth_helper.fake_user_session_info(), session)

        elif not auth_helper.is_logged_in(session, current_app):
            token = request.args.get("token")
            if token:
                user_data = mavis_helper.verify_token(token, current_app)
                auth_helper.log_user_in(user_data, session)
            else:
                target_url = mavis_helper.mavis_url(
                    current_app,
                    "/start?redirect_after_login=" + urllib.parse.quote(request.url),
                )
                return redirect(target_url)

        return f(*args, **kwargs)

    return decorated_function


@main.route("/")
@login_required
def index():
    return render_template("index.jinja")
