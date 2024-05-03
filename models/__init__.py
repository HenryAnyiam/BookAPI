from models.model import Base, Book, BookModel
from models.engine import engine, Session


Base.metadata.create_all(engine, checkfirst=True)
