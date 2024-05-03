from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine("sqlite+pysqlite:///bookdb.db",
                       pool_pre_ping=True)
session = sessionmaker(engine)
Session = scoped_session(session)
