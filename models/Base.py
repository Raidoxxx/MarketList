from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://root:@localhost:3306/marketlistapp',
    echo=True
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(bind=engine)

# Mixin para adicionar created_at e updated_at a quem herdar
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
