from datetime import datetime, timedelta, timezone
from flask import session
import urllib.parse

def it_redirects_to_mavis_start(response):
    # Check that the response had a redirect code.
    assert response.status_code == 302
    redirect_to = response.headers['Location'] 
    assert redirect_to.startswith( 'http://mavis-root.localhost/' )
    assert "/start" in redirect_to;
    # Check that the return_url param is on the redirect
    parsed_url = urllib.parse.urlparse(redirect_to)
    assert 'redirect_after_login=' in parsed_url.query
    return True

def test_when_session_has_a_user_id_and_is_not_expired_it_does_not_redirect(client):
    with client.session_transaction() as session:
        # set session vars without going through the login route
        session["user_id"] = 1
        session["last_visit"] = datetime.now().astimezone(timezone.utc) - timedelta(minutes=1)

    response = client.get("/")
    assert response.status_code == 200

def test_when_session_has_a_user_id_but_is_expired_it_redirects_to_mavis_start(client):
    with client.session_transaction() as session:
        # set session vars without going through the login route
        session["user_id"] = 1
        session["last_visit"] = datetime.now().astimezone(timezone.utc) - timedelta(hours=101)

    response = client.get("/")
    assert it_redirects_to_mavis_start(response)

def test_when_user_id_not_in_session_it_redirects_to_mavis_sign_in(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session.pop("user_id", None)

    response = client.get("/", follow_redirects=False)
    assert it_redirects_to_mavis_start(response)

 