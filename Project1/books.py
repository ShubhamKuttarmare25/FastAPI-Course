from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title':'title1', 'author':'author1', 'category': 'science'},
    {'title':'title2', 'author':'author2', 'category': 'journal'},
    {'title':'title3', 'author':'author3', 'category': 'history'},
    {'title':'title4', 'author':'author1', 'category': 'history'},
    {'title':'title5', 'author':'author1', 'category': 'science'},
    {'title':'title6', 'author':'author6', 'category': 'journal'},
    {'title':'title7', 'author':'author7', 'category': 'science'},
]

@app.get('/api-endpoint')
async def first_api():
    return {'message': 'First api'}

@app.get('/get-all-books')
async def get_all_books():
    return BOOKS

#static api
@app.get('/books/my-book')  # it will take this as dynamic_param and will return the {"dynamic_param": dynamic_param} so to avoid this we need to put it above dynamic param req.
async def read_all_books():
    return {'book_title': "My Favorite book"}

#get the book by title
@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in BOOKS:
        if(book.get("title").casefold() == book_title.casefold()):
            return book
        

#path parameters
@app.get('/books/{dynamic_param}')
async def read_all_books(dynamic_param: str): # explicit type attach to this param must be a string
    return {'dynamic_param': dynamic_param}




#query param 
@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = [] #empty list to return 
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return    



#assignment
# #2 using query param # need to move this ahead
@app.get("/books/byauthor/")
async def get_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return



#using path param and query param 
@app.get("/books/{author_name}/")
async def read_book_by_author_name(author_name: str, category: str):
    books_to_return1 = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold() and book.get("category").casefold() == category.casefold():
            books_to_return1.append(book)
    return books_to_return1




#using post 
@app.post("/books/create-book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)




#using put request method

@app.put("/books/update-book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book



#delete request method 

@app.delete("/books/delete-book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break









#assinment

#1 using path param
@app.get("/books/byauthor/{author}")
async def get_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return



