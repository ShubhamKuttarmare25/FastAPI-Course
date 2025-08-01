from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ✅ Define a Pydantic model for request validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)  # rating must be 0 to 5
    published_at: int = Field(gt=1999, lt=2021)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Book",
                "author": "codewithroby",
                "description": "A new description of book",
                "rating": 5,
                "published_at": 2020
            }
        }
    }


# ✅ Book class (could be replaced with a Pydantic model for better serialization)
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_at: int

    def __init__(self, id, title, author, description, rating, published_at):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_at = published_at


# ✅ Ratings corrected (must be between 0 and 5)
BOOKS = [
    Book(1, 'Computer Science', "codingWithRoby", "A very good book", 2, 2004),
    Book(2, 'Environmental Science', "envWithRoby", "A very good book to learn about environment", 5, 2005),
    Book(3, 'Electronics journal', "Elex Current", "Book related to current mechanics", 4, 2010),  # rating fixed
    Book(4, 'SQL Journal', "sqlwithRoby", "Book for sql queries", 3, 2011),                        # rating fixed
    Book(5, 'Get ready English', "englishwithMik", "get fluent in english", 3, 2018),              # rating fixed
    Book(6, 'Get ready German', "germanwithRob", "Learn awesome vocab of german language", 1, 2020) # rating fixed
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# ✅ Added return statement for confirmation
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    return new_book  # ✅ return the newly created book


# ✅ Helper function to auto-assign book ID
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": "Book not found"}  # ✅ good to add fallback


# ✅ Corrected query param route (both /books and /books/)
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]
    return books_to_return


# ✅ FIXED missing `/` in path and added return statement
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.dict())  # ✅ update the book object
            return {"message": "Book updated successfully", "book": BOOKS[i]}
    return {"message": "Book not found"}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": f"Book with ID {book_id} deleted successfully"}
    return {"message": "Book not found"}


# ✅ FIXED missing `/` and added return
@app.get("/book/publish/")
async def get_book_by_year(published_at: int):
    books_to_return = [book for book in BOOKS if book.published_at == published_at]
    return books_to_return
