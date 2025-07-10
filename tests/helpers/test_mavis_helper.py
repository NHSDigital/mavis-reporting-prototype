import pytest
from flask import current_app

from mavis_reporting.helpers import mavis_helper

from mavis_reporting import create_app


def test_mavis_url_with_just_path(app):
    with app.app_context():
        app.config["MAVIS_ROOT_URL"] = "http://i.am.mavis:4000/"
        url = mavis_helper.mavis_url(current_app, "/some/path.json")
        assert url == "http://i.am.mavis:4000/some/path.json"


def test_mavis_url_with_path_and_params(app):
    with app.app_context():
        app.config["MAVIS_ROOT_URL"] = "http://i.am.mavis:4000/"
        url = mavis_helper.mavis_url(
            current_app, "/some/path.json", {"param1": "param 1 value"}
        )
        assert url == "http://i.am.mavis:4000/some/path.json?param1=param+1+value"


def test_mavis_url_with_path_and_multiple_params(app):
    with app.app_context():
        app.config["MAVIS_ROOT_URL"] = "http://i.am.mavis:4000/"
        url = mavis_helper.mavis_url(
            current_app,
            "/some/path.json",
            {"param1": "param 1 value", "param2": 123, "param3": "something else"},
        )
        assert (
            url
            == "http://i.am.mavis:4000/some/path.json?param1=param+1+value&param2=123&param3=something+else"
        )


def test_that_mavis_url_applies_url_encoding_to_params(app):
    with app.app_context():
        app.config["MAVIS_ROOT_URL"] = "http://i.am.mavis:4000/"
        url = mavis_helper.mavis_url(
            current_app,
            "/some/path.json",
            {"return_url": "https://some.other.domain/login?token=123"},
        )
        assert (
            url
            == "http://i.am.mavis:4000/some/path.json?return_url=https%3A%2F%2Fsome.other.domain%2Flogin%3Ftoken%3D123"
        )
