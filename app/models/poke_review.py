import uuid
from app import db

class PokeReview(db.Model):
    __tablename__ = "poke_review"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    star = db.Column(db.SmallInteger, nullable=False,default=0)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    pokemon_name = db.Column(db.String, nullable=False)
    user_ip = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, nullable=True, onupdate=db.func.current_timestamp()
    )



  