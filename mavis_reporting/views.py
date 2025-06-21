from flask import Blueprint, render_template
import logging

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")
