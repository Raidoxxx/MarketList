from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base, TimestampMixin

class Item(Base, TimestampMixin):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable=False)
    check = Column(Integer, default=0)
    
    list = relationship('List', back_populates='items')

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', list_id={self.list_id})>"
