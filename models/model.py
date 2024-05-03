from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Book(Base):
    """class to map to table book"""

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    isbn: Mapped[str]

    def to_dict(self) -> dict:
        """returns a dictionary representation of the instance"""

        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


class BookModel(BaseModel):
    """type model for Book class"""

    title: str
    author: str
    year: int
    isbn: str

    class Config:
        partial = True
        extra = "ignore"
