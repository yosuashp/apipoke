import traceback
from flask import make_response, jsonify, current_app, request
from flask_restful import Resource, reqparse
from flask_sieve import Validator
from app.models.poke_review import PokeReview
from app import db 
from datetime import datetime

class AllReviews(Resource):
    @classmethod
    def get(cls):
        try:
            reviews = PokeReview.query.all()
            if reviews:
                serialized_reviews = []
                for review in reviews:
                    serialized_review = {
                        'id': str(review.id),
                        'star': review.star,
                        'title': review.title,
                        'content': review.content,
                        'pokemon_name': review.pokemon_name,
                        'user_ip': review.user_ip,
                        'user_agent': review.user_agent.decode('utf-8'),
                        'created_at': review.created_at.isoformat(),
                        'updated_at': review.updated_at.isoformat() if review.updated_at else None
                    }
                    serialized_reviews.append(serialized_review)

                return make_response(jsonify(serialized_reviews), 200)
            else:
                return make_response(jsonify({'error': 'No reviews found'}), 404)
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
