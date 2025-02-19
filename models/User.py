# models/User.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from models.Base import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    
    # Adiciona o relacionamento com a model List
    lists = relationship('List', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)
