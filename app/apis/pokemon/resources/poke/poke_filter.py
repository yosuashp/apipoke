# import requests
# from flask import jsonify, request
# from flask_restful import Resource

# class PokemonFilterResource(Resource):
#     @classmethod
#     def get_pokemon_categories(cls, pokemon_species_id):
#         try:
#             response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_species_id}/')
#             if response.status_code == 200:
#                 pokemon_data = response.json()

#                 categories = {
#                     "gender_rate": pokemon_data.get("gender_rate", "Unknown"),
#                     "capture_rate": pokemon_data.get("capture_rate", "Unknown"),
#                     "base_happiness": pokemon_data.get("base_happiness", "Unknown"),
#                     "hatch_counter": pokemon_data.get("hatch_counter", "Unknown"),
#                     "id": pokemon_data.get("id", "Unknown"),
#                     "name": pokemon_data.get("name", "Unknown")
#                 }

#                 return categories
#             else:
#                 return {"error": "Failed to fetch pokemon species data"}
#         except Exception as e:
#             return {"error": str(e)}

#     @classmethod
#     def get_pokemon_list(cls, category):
#         try:
#             # Memecah string category menjadi dua bagian
#             category_parts = category.split(':')

#             # Memastikan ada dua bagian yang telah dipisahkan
#             if len(category_parts) != 2:
#                 return {'error': 'Invalid category format'}, 400

#             # Mengambil nilai kategori (bagian kedua)
#             category_value = category_parts[1]

#             response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100&offset=0/')
#             if response.status_code == 200:
#                 pokemon_data = response.json()['results']

#                 # Mengambil nama-nama Pokemon
#                 pokemon_names = [pokemon['name'] for pokemon in pokemon_data]
#                 # Mengurutkan nama-nama Pokemon secara ascending
#                 pokemon_names.sort()

#                 filtered_pokemon = []
#                 for pokemon_name in pokemon_names:
#                     pokemon_id = pokemon_name
#                     categories = cls.get_pokemon_categories(pokemon_id)

#                     # Memeriksa apakah kategori yang diterima sesuai dengan kategori pokemon
#                     if categories.get(category_parts[0], "Unknown") == int(category_value):
#                         pokemon_info = {
#                             "name": pokemon_name,
#                             "category": categories
#                         }
#                         filtered_pokemon.append(pokemon_info)

#                 # Jika tidak ada pokemon yang sesuai dengan kategori, kembalikan pesan kesalahan
#                 if not filtered_pokemon:
#                     return {'error': 'No Pokemon found for the provided category'}, 404

#                 # Jika ada pokemon yang sesuai, kembalikan daftar pokemon
#                 return {'pokemon': filtered_pokemon}, 200

#             else:
#                 return {'error': 'Failed to fetch pokemon data'}, 500

#         except Exception as e:
#             return {'error': str(e)}, 500


#     def get(self):
#         try:
#             category = request.args.get('category')
#             if not category:
#                 return jsonify({'error': 'Please provide a category'}), 400

#             # Panggil metode get_pokemon_list dengan parameter kategori
#             filtered_pokemon_data, status_code = self.get_pokemon_list(category)
#             return filtered_pokemon_data, status_code  # Mengembalikan respons tanpa jsonify
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

import requests
from flask import jsonify, request
from flask_restful import Resource

class PokemonFilterResource(Resource):
    @classmethod
    def get_pokemon_categories(cls, pokemon_species_id):
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_species_id}/')
            if response.status_code == 200:
                pokemon_data = response.json()

                categories = {
                    "gender_rate": pokemon_data.get("gender_rate", "Unknown"),
                    "capture_rate": pokemon_data.get("capture_rate", "Unknown"),
                    "base_happiness": pokemon_data.get("base_happiness", "Unknown"),
                    "hatch_counter": pokemon_data.get("hatch_counter", "Unknown"),
                    "id": pokemon_data.get("id", "Unknown"),
                    "name": pokemon_data.get("name", "Unknown")
                }

                return categories
            else:
                return {"error": "Failed to fetch pokemon species data"}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def get_pokemon_list(cls, category_type, category_value):
        try:
            response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=50&offset=0/')
            if response.status_code == 200:
                pokemon_data = response.json()['results']

                # Mengambil nama-nama Pokemon
                pokemon_names = [pokemon['name'] for pokemon in pokemon_data]
                # Mengurutkan nama-nama Pokemon secara ascending
                pokemon_names.sort()

                filtered_pokemon = []
                for pokemon_name in pokemon_names:
                    pokemon_id = pokemon_name
                    categories = cls.get_pokemon_categories(pokemon_id)

                    # Memeriksa apakah kategori yang diterima sesuai dengan kategori pokemon
                    if categories.get(category_type, "Unknown") == int(category_value):
                        pokemon_info = {
                            "name": pokemon_name,
                            "category": categories
                        }
                        filtered_pokemon.append(pokemon_info)

                # Jika tidak ada pokemon yang sesuai dengan kategori, kembalikan pesan kesalahan
                if not filtered_pokemon:
                    return {'error': f'No Pokemon found for the provided {category_type}'}, 404

                # Jika ada pokemon yang sesuai, kembalikan daftar pokemon
                return {'pokemon': filtered_pokemon}, 200

            else:
                return {'error': 'Failed to fetch pokemon data'}, 500

        except Exception as e:
            return ({'error': str(e)}), 500
        
    def get(self):
        try:
            # Mendapatkan nilai capture_rate dari parameter query
            capture_rate = request.args.get('capture_rate')

            if not capture_rate:
                return {'error': 'Please provide capture_rate in the query parameters'}, 400

            # Panggil metode get_pokemon_list dengan parameter capture_rate
            filtered_pokemon_data, status_code = self.get_pokemon_list('capture_rate', capture_rate)
            return filtered_pokemon_data, status_code  # Mengembalikan respons tanpa jsonify

        except Exception as e:
            return {'error': 'An error occurred while processing your request'}, 500
