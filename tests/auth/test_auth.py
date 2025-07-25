from datetime import datetime, timedelta, timezone
from flask import session
from os import urandom
from unittest import mock


import urllib.parse


def configure_app(app):
    app.config.update(
        {
            "TESTING": True,
            "CLIENT_ID": random_token(),
            "CLIENT_SECRET": random_token(),
        }
    )


def random_token():
    return urandom(16).hex()


def default_url():
    return "/reporting/default"


def it_redirects_to_mavis_start(response):
    # Check that the response had a redirect code.
    assert response.status_code == 302
    redirect_to = response.headers["Location"]
    assert redirect_to.startswith("http://mavis-root.localhost/")
    assert "/start" in redirect_to
    # Check that the return_url param is on the redirect
    parsed_url = urllib.parse.urlparse(redirect_to)
    assert "redirect_uri=" in parsed_url.query
    return True


def test_when_session_has_a_user_id_and_is_not_expired_it_does_not_redirect(
    app, client
):
    with app.app_context():
        configure_app(app)
        with client.session_transaction() as session:
            # set session vars without going through the login route
            session["user_id"] = 1
            session["last_visit"] = datetime.now().astimezone(timezone.utc) - timedelta(
                minutes=1
            )

        response = client.get(default_url())
        assert response.status_code == 200


def test_when_session_has_a_user_id_but_is_expired_it_redirects_to_mavis_start(client):
    with client.session_transaction() as session:
        # set session vars without going through the login route
        session["user_id"] = 1
        session["last_visit"] = datetime.now().astimezone(timezone.utc) - timedelta(
            hours=101
        )

    response = client.get(default_url())
    assert it_redirects_to_mavis_start(response)


def test_when_user_id_not_in_session_it_redirects_to_mavis_sign_in(client):
    with client.session_transaction() as session:
        # set user_id session var without going through the login route
        session["user_id"] = None

    response = client.get(default_url(), follow_redirects=False)
    assert it_redirects_to_mavis_start(response)


@mock.patch(
    "mavis_reporting.helpers.auth_helper.fake_login_enabled",
    mock.MagicMock(return_value=True),
)
def test_when_fake_login_is_enabled_it_logs_in_as_nurse_joy_without_a_redirect(
    app, client
):
    with app.app_context():
        configure_app(app)
        with client:
            # with client.session_transaction() as session:
            response = client.get(default_url(), follow_redirects=False)
            assert response.status_code == 200
            assert session["user_id"] == 1
            assert session["user"]["email"] == "nurse.joy@example.com"
