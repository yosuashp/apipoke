from flask import Blueprint
from .resources.poke.poke_list import PokeList
from .resources.poke.poke_detail import PokeDetail
from .resources.poke.poke_review import Review
from .resources.poke.poke_allreview import AllReviews
from .resources.poke.poke_search import Search
from .resources.poke.poke_filter import PokemonFilterResource

def initialize_routes(api):
    api.add_resource(PokeList, '/v1')
    api.add_resource(PokeDetail, '/v1/<name>')
    api.add_resource(Review, '/v1/<name>/review', endpoint='review_by_name')
    api.add_resource(Review, '/v1/review/<name>', endpoint='review_by_name_v1')
    api.add_resource(AllReviews, '/v1/reviews')
    api.add_resource(Search, '/v1/search')
    api.add_resource(PokemonFilterResource, '/v1/filters/list')
