from flask import Blueprint, render_template
import logging

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    unused = 3
    return render_template("index.jinja")
