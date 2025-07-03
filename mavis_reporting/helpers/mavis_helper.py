import requests
import urllib.parse

def mavis_url(current_app, path):
    return urllib.parse.urljoin( current_app.config['MAVIS_ROOT_URL'], path )

def verify_token(token, current_app):
    url = mavis_url(current_app, '/tokens/' + token)
    user_data = None

    headers = {'Authorization' :current_app.config['SECRET_KEY']}
    r = requests.get(url, headers=headers)

    user_data = r.json()

    return user_data