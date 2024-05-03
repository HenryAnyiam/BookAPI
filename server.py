from fastapi import FastAPI, Request, HTTPException
from models import Session, Book, BookModel

app = FastAPI(strict_slashes=False,
              title="Book Collection API",
              description="This is a documentation for\
                      an API with CRUD routes for a book collection")


@app.get("/books")
async def all_books():
    """Get all books stored in the database"""
    with Session() as session:
        books = session.query(Book).all()

    return books


@app.get("/books/{id}")
async def get_book(id: int):
    """Get book detail by id"""

    with Session() as session:
        book = session.get(Book, id)
        if not book:
            raise HTTPException(status_code=404,
                                detail=f"No data found for book with Id {id}")

    return book


@app.post("/books")
async def create_book(book: BookModel):
    """Create new book and add to the collection"""

    with Session() as session:
        new_book = Book(title=book.title,
                        author=book.author,
                        year=book.year,
                        isbn=book.isbn)
        session.add(new_book)
        session.commit()
        book_dict = new_book.to_dict()

    return book_dict


@app.put("/books/{id}")
async def update_book(id: int, book: dict):
    """Update a book detail by id"""

    with Session() as session:
        book_detail = session.get(Book, id)
        if not book_detail:
            raise HTTPException(status_code=404,
                                detail=f"No data found for book with Id {id}")
        allowed = ["title", "year", "author", "isbn"]
        for key, value in book.items():
            if key in allowed:
                if ((key == "year" and isinstance(value, int)) or
                        (key != "year" and isinstance(value, str))):
                    setattr(book_detail, key, value)
                else:
                    raise HTTPException(status_code=422,
                                        detail=f"Incorrect DataType for {key}")
            else:
                raise HTTPException(status_code=422,
                                    detail=f"Unknown Column {key}")
        session.commit()
        book_dict = book_detail.to_dict()

    return book_dict


@app.delete("/books/{id}")
async def delete_book(id: int):
    """delete book by given id"""

    with Session() as session:
        book = session.get(Book, id)
        if not book:
            raise HTTPException(status_code=404,
                                detail=f"No data found for book with Id {id}")
        session.delete(book)
        session.commit()

    return {f"Message": f"Book with {id} deleted"}
