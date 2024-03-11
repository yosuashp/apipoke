import requests
from flask_restful import Resource

class PokeList(Resource):
    @classmethod
    def get_pokemon_species_info(cls, pokemon_id):
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/')
            if response.status_code == 200:
                pokemon_species_data = response.json()

                species_info = {
                    "id": pokemon_species_data.get("id"),
                    "name": pokemon_species_data.get("name"),
                    "order": pokemon_species_data.get("order"),
                    "gender_rate": pokemon_species_data.get("gender_rate"),
                    "capture_rate": pokemon_species_data.get("capture_rate"),
                    "base_happiness": pokemon_species_data.get("base_happiness"),
                    "is_baby": pokemon_species_data.get("is_baby"),
                    "is_legendary": pokemon_species_data.get("is_legendary"),
                    "is_mythical": pokemon_species_data.get("is_mythical"),
                    "hatch_counter": pokemon_species_data.get("hatch_counter"),
                    "has_gender_differences": pokemon_species_data.get("has_gender_differences"),
                    "forms_switchable": pokemon_species_data.get("forms_switchable"),
                    "home": cls.get_pokemon_home(pokemon_id)
                }

                return species_info
            else:
                return {"error": "Failed to fetch pokemon species data"}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def get_pokemon_home(cls, pokemon_id):
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/')
            if response.status_code == 200:
                pokemon_data = response.json()
                home_info = pokemon_data.get("sprites", {}).get("other", {}).get("home", {})
                return home_info
            else:
                return {"error": "Failed to fetch pokemon home data"}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def get(cls):
        try:
            pokemon_list_response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=50&offset=0/')
            if pokemon_list_response.status_code == 200:
                pokemon_list_data = pokemon_list_response.json()['results']
                pokemon_species_info_list = []

                for pokemon_info in pokemon_list_data:
                    pokemon_name = pokemon_info['name']
                    species_info = cls.get_pokemon_species_info(pokemon_name)
                    pokemon_species_info_list.append(species_info)

                # Sorting the pokemon species info list by 'name' in descending order
                sorted_pokemon_species_info_list = sorted(pokemon_species_info_list, key=lambda x: x['name'], reverse=True)

                return(sorted_pokemon_species_info_list), 200
            else:
                return({'error': 'Failed to fetch pokemon list data'}), 500

        except Exception as e:
            return ({'error': str(e)}), 500
