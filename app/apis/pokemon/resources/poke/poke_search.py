import requests
import traceback
from flask import make_response, jsonify, current_app, request
from flask_restful import Resource

class Search(Resource):
    @classmethod
    def get(cls):
        try:
            search_params = dict(request.args)
            pokemon_name_or_id = search_params.get('name') or search_params.get('id')
            if not pokemon_name_or_id:
                return make_response(jsonify({'error': 'Please provide a name or an ID.'}), 400)

            search_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}/'

            r = requests.get(search_url)
            if r.status_code == 404:
                return make_response(jsonify({'error': 'Pokemon not found.'}), 404)
            elif not r.ok:
                return make_response(jsonify({'error': 'Failed to fetch Pokemon data.'}), r.status_code)

            pokemon_data = r.json()

            abilities_data = pokemon_data.get('abilities', [])
            height_data = pokemon_data.get('height', '')
            weight_data = pokemon_data.get('weight', '')
            held_items_data = pokemon_data.get('held_items', [])
            name_data = pokemon_data.get('name', '')
            id_data = pokemon_data.get('id', '')
            types_data = pokemon_data.get('types', [])
            species_data = pokemon_data.get('species', {})

            
            response_data = {
                'abilities': abilities_data,
                'height': height_data,
                'weight': weight_data,
                'held_items': held_items_data,
                'name': name_data,
                'id': id_data,
                'types': types_data,
                'species': species_data
            }

            return make_response(jsonify(response_data), r.status_code)

        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)




