import jwt
import requests
import urllib.parse

from flask import abort, redirect, request


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
    r = requests.get(url, headers=headers)

    token_data = r.json()
    jwt_data = jwt.decode(token_data["jwt"], secret, algorithms="HS512")
    session["jwt"] = token_data["jwt"]
    return jwt_data["data"]


def api_call(current_app, session, request, path, params={}):
    url = mavis_url(current_app, path, params)
    headers = {
        "Authorization": "Bearer " + session["jwt"],
        "Content-type": "application/json; charset=utf-8",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        login_and_return_after(current_app, url)

    return response


def login_and_return_after(current_app, path):
    target_url = mavis_url(
        current_app,
        "/start?redirect_after_login=" + urllib.parse.quote(path),
    )
    current_app.logger.warn("REDIRECTING TO ", target_url)
    return redirect(target_url)
