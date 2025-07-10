import jwt
import requests
import urllib.parse
import werkzeug

from flask import abort, redirect, request

from werkzeug.exceptions import Unauthorized


def mavis_url(current_app, path, params={}):
    url = urllib.parse.urljoin(current_app.config["MAVIS_ROOT_URL"], path)
    if params != {}:
        parsed_url = urllib.parse.urlsplit(url)
        query_string = urllib.parse.urlencode(params)
        url_with_params = parsed_url._replace(query=query_string)
        url = urllib.parse.urlunsplit(url_with_params)

    return url


def verify_token(token, current_app, session):
    url = mavis_url(current_app, "/tokens/" + token)
    secret = current_app.config["SECRET_KEY"]

    headers = {"Authorization": secret}
    r = make_request(url, headers=headers)

    token_data = r.json()
    jwt_data = jwt.decode(token_data["jwt"], secret, algorithms="HS512")
    session["jwt"] = token_data["jwt"]
    return jwt_data["data"]


def api_call(current_app, session, path, params={}):
    url = mavis_url(current_app, path, params)
    headers = {
        "Authorization": "Bearer " + session["jwt"],
        "Content-type": "application/json; charset=utf-8",
    }
    response = make_request(url, headers=headers)
    if response.status_code == 401 or response.status_code == 403:
        session.clear()
        raise (werkzeug.exceptions.Unauthorized)

    return response


def login_and_return_after(current_app, return_url):
    target_url = mavis_url(
        current_app,
        "/start?redirect_after_login=" + urllib.parse.quote_plus(return_url),
    )
    current_app.logger.warning("REDIRECTING TO %s", target_url)
    return redirect(target_url)


def make_request(url, headers):
    return requests.get(url, headers=headers)
