from fastapi import FastAPI
from pydantic import BaseModel, Field # this is added for the validation it is preinstalled with fastapi
from typing import Optional





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


class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "ID is not needed on create", default = None)
    title : str = Field(min_length = 3)
    author : str = Field(min_length = 1)
    description : str = Field(min_length = 1, max_length = 100)
    rating : int = Field(gt = -1 , lt = 6)

    # this is used to show the default values (in the example section)
    model_config ={
        "json_schema_extra":{
            "example":{
                "title": "A new Book",
                "author": "codewithroby",
                "description":"A new description of book",
                "rating": 5
            }
        }
    }



            
# an empty list for the books

BOOKS = [

    Book(1, 'Computer Science', "codingWithRoby", "A very good book", 5),
    Book(2, 'Environmental Science', "envWithRoby", "A very good book to learn about environment", 5),
    Book(3, 'Electronics journal', "Elex Current", "Book related to current mechanics" ,8),
    Book(4, 'SQL Journal', "sqlwithRoby", "Book for sql queries", 7),
    Book(5, 'Get ready English ', "englishwithMik", "get fluent in english", 6),
    Book(6, 'Get ready German', "germanwithRob", "Learn awesome vocab of german language", 6)
    
]



@app.get("/books")
async def read_all_books():
    return BOOKS



@app.post("/create_book")
async def create_book(book_request : BookRequest): #using body this does not add any type of validation to the values
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book: Book):
    # if(len(BOOKS) > 0):
    #     book.id = BOOKS[-1].id + 1
    # else :
    #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

