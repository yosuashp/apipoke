
import requests
import traceback
from flask import make_response, jsonify, current_app
from flask_restful import Resource
from flask_sieve import Validator

class PokeDetail(Resource):
    @classmethod
    def get(cls, name):
        try:
            rules = {
                'name': ['required', 'alpha']
            }
            messages = {
                'name.required': 'Yikes! The name is required',
                'name.alpha': 'Yikes! The name must be a string',
            }
            
            validator = Validator(rules=rules, messages=messages, request={'name': name})
            if validator.passes():
                get_pokemon_name_url = f'https://pokeapi.co/api/v2/pokemon/{name}'
                r = requests.get(get_pokemon_name_url)
                return r.json()
            else:
                return make_response(jsonify(validator.messages()), 400)
        except Exception as e:  
            current_app.logger.error(traceback.format_exc())
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
