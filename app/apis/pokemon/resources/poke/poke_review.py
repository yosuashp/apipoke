import traceback
import uuid
from flask import make_response, jsonify, current_app, request
from flask_restful import Resource
from flask_sieve import Validator
from app.models.poke_review import PokeReview
from app import db 


class Review(Resource):
    @classmethod
    def post(cls, name):
        try:
            rules = {
                'star': ['required', 'numeric'], 
                'title': ['required', 'string'],
                'content': ['required', 'string']
            }
            # messages = {
            #     'name.required': 'Yikes! The name is required',
            #     'name.alpha': 'Yikes! The name must be a string',
            # }
            
            validator = Validator(rules=rules, request=request)
            if validator.passes():
                user = PokeReview(
                    id = uuid.uuid4(),
                    star=request.json['star'],
                    title=request.json['title'],
                    content=request.json['content'],
                    pokemon_name = name,
                    user_ip=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                db.session.add(user)
                db.session.commit()

                return make_response(jsonify({'message': 'success'}),200)
            else:
                return make_response(jsonify(validator.messages()), 400)
        except Exception as e:  
            current_app.logger.error(traceback.format_exc())
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)

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
                reviews = PokeReview.query.filter_by(pokemon_name=name).all()
                serialized_reviews = []
                for review in reviews:
                    serialized_review = {
                        'id': str(review.id),
                        'star': review.star,
                        'title': review.title,
                        'content': review.content,
                        'pokemon_name': review.pokemon_name,
                        'user_ip': review.user_ip,
                        'user_agent': review.user_agent,
                        'created_at': review.created_at.isoformat(),
                        'updated_at': review.updated_at.isoformat() if review.updated_at else None
                    }
                    serialized_reviews.append(serialized_review)

                return make_response(jsonify(serialized_reviews), 200)
            else:
                return make_response(jsonify(validator.messages()), 400)
        except Exception as e:  
            current_app.logger.error(traceback.format_exc())
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
