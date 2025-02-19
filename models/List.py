from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base, TimestampMixin

class List(Base, TimestampMixin):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship('User', back_populates='lists')
    items = relationship('Item', back_populates='list', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<List(id={self.id}, name='{self.name}', user_id={self.user_id})>"
