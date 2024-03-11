from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

pokemonApp = Blueprint("pokemon", __name__, template_folder="templates", url_prefix="/pokemon")
pokemon_app = Api(pokemonApp)
initialize_routes(pokemon_app)