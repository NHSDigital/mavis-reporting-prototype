from jinja2 import FileSystemLoader, ChoiceLoader, PackageLoader, ChainableUndefined
import os


def configure_jinja2(app):
    app.jinja_options = {
        "undefined": ChainableUndefined,  # This is needed to prevent jinja from throwing an error when chained parameters are undefined
        "loader": ChoiceLoader(
            [
                FileSystemLoader(os.path.join(app.root_path, "templates")),
                PackageLoader(
                    "nhsuk_frontend_jinja", package_path="templates/components"
                ),
                PackageLoader("nhsuk_frontend_jinja", package_path="templates/macros"),
                PackageLoader("nhsuk_frontend_jinja"),
            ]
        ),
    }
    return app
