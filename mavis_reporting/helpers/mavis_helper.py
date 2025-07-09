import jwt
import requests
import urllib.parse


def mavis_url(current_app, path, params={}):
    url = urllib.parse.urljoin(current_app.config["MAVIS_ROOT_URL"], path)
    if params != {}:
        parsed_url = urllib.parse(url)
        url_with_params = parsed_url._replace(query=params)
        url = urllib.parse.urlunparse(url_with_params)

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


def api_call(current_app, session, path, params={}):
    url = mavis_url(current_app, path, params)
    headers = {
        "Authorization": "Bearer " + session["jwt"],
        "Content-type": "application/json; charset=utf-8",
    }
    return requests.get(url, headers=headers)
