from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./threat_intelligence.db"

engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread" : False}

)

class Base(DeclarativeBase):
    pass


class Scan(Base):

    __tablename__ = "scans"

    id = Column(Integer, primary_key = True)
    target = Column(String)
    target_type = Column(String)
    results = Column(JSON)
    ai_analysis = Column(String)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()