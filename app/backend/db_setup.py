from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class KeyValue(Base):
    __tablename__ = "key_value_store"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class KeyValueRevision(Base):
    __tablename__ = "key_value_revisions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_value_id = Column(Integer, ForeignKey("key_value_store.id"), nullable=False)
    revision_number = Column(Integer, nullable=False)
    value = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now())

# Database setup
def get_engine(db_url="sqlite:///kv_store.db"):
    return create_engine(db_url)

def init_db(engine):
    Base.metadata.create_all(engine)

# Session maker
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
