from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

class PreBase:
    pass

Base = declarative_base(cls=PreBase)

DBEngine = create_engine('sqlite:///global_progress.db', echo=False)
Session = sessionmaker(bind=DBEngine)


def init_db():
    Base.metadata.create_all(bind=DBEngine)
    print('[SYSTEM] SQLite DB initialized')