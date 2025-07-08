import jwt
import requests
import urllib.parse


def mavis_url(current_app, path):
    return urllib.parse.urljoin(current_app.config["MAVIS_ROOT_URL"], path)


def verify_token(token, current_app):
    url = mavis_url(current_app, "/tokens/" + token)
    user_data = None
    secret = current_app.config["SECRET_KEY"]

    headers = {"Authorization": secret}
    r = requests.get(url, headers=headers)

    token_data = r.json()
    jwt_data = jwt.decode(token_data["jwt"], secret, algorithms="HS512")

    return jwt_data["data"]
