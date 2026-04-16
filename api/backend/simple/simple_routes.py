from flask import Blueprint, jsonify, current_app, redirect, url_for
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

# This blueprint handles basic routes useful for testing and demonstration
simple_routes = Blueprint("simple_routes", __name__)


# ------------------------------------------------------------
# / is the most basic route
# Once the api container is started, in a browser, go to
# localhost:4000/