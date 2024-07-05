from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(120))
    price = db.Column(db.Float, nullable=True) 

    def __init__(self, name, image=None, price=None):
        self.name = name
        self.image = image
        self.price = price
