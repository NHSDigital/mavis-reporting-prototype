from datetime import datetime, timedelta, timezone
import logging
import sys
import urllib

from flask import (
    request,
    session,
    redirect,
    current_app,
)

from functools import wraps

from mavis_reporting.helpers import mavis_helper


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if fake_login_enabled(current_app):
            current_app.logger.warning(
                "FAKE_LOGIN_ENABLED! Logging in as fake_user_session_info"
            )
            log_user_in(fake_user_session_info(), session)

        elif not is_logged_in(session, current_app):
            current_app.logger.info("NOT logged in")
            token = request.args.get("token")
            if token:
                user_data = mavis_helper.verify_token(token, current_app, session)
                log_user_in(user_data, session)
                return redirect(
                    url_helper.url_without_param(request.full_path, "token")
                )
            else:
                current_app.logger.info("no token given")
                target_url = mavis_helper.mavis_url(
                    current_app,
                    "/start?redirect_after_login=" + urllib.parse.quote(request.url),
                )
                return redirect(target_url)

        return f(*args, **kwargs)

    return decorated_function


def session_expired(session, current_app):
    last_visit = session.get("last_visit")
    if last_visit is None:
        return True

    session_age = (datetime.now().astimezone(timezone.utc) - last_visit).total_seconds()
    return abs(session_age) > current_app.config["SESSION_TTL_SECONDS"]


def is_logged_in(session, current_app):
    if "user_id" in session:
        if session_expired(session, current_app):
            session.clear()
            return False
        else:
            session["last_visit"] = datetime.now().astimezone(timezone.utc)
            return True

    else:
        return False


def log_user_in(data, session):
    session["last_visit"] = datetime.now().astimezone(timezone.utc)
    session["cis2_info"] = data["cis2_info"]
    session["user"] = data["user"]
    session["user_id"] = data["user"]["id"]


def fake_login_enabled(current_app):
    return bool(current_app.config.get("FAKE_LOGIN_ENABLED"))


def fake_user_session_info():
    return {
        "user_id": 1,
        "created_at": datetime.now() - timedelta(minutes=5),
        "last_visit": datetime.now() - timedelta(minutes=1),
        "user": {
            "id": 1,
            "email": "nurse.joy@example.com",
            "created_at": "2025-06-16T11:09:24.289+01:00",
            "updated_at": "2025-07-04T10:11:36.100+01:00",
            "provider": None,
            "uid": None,
            "given_name": "Nurse",
            "family_name": "Joy",
            "session_token": None,
            "fallback_role": "nurse",
        },
        "cis2_info": {
            "selected_org": {"code": "R1L", "name": "SAIS Organisation 1"},
            "selected_role": {
                "code": "S8000:G8000:R8001",
                "workgroups": ["schoolagedimmunisations"],
            },
        },
    }
