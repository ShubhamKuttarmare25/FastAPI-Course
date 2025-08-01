from fastapi import FastAPI, Body

app = FastAPI()


#created the object of the book
class Book:
    id : int
    title : str
    author: str
    description : str
    rating : int 

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
            
# an empty list for the books

BOOKS = [

    Book(1, 'Computer Science', "codingWithRoby", "A very good book", 5),
    Book(2, 'Environmental Science', "envWithRoby", "A very good book to learn about environment", 5),
    Book(3, 'Electronics journal', "Elex Current", "Book related to current mechanics" ,8),
    Book(4, 'SQL Journal', "sqlwithRoby", "Book for sql queries", 7),
    Book(5, 'Get ready English ', "englishwithMik", "get fluent in english", 6)
    
]



@app.get("/books")
async def read_all_books():
    return BOOKS



@app.post("/create_book")
async def create_book(book_request = Body()): #using body this does not add any type of validation to the values
    BOOKS.append(book_request)
