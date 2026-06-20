from flask import Blueprint

bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications",
    template_folder="templates",
)

from . import routes
