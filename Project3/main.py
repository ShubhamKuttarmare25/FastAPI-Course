# root folder where we create fastapi application

from fastapi import FastAPI, Depends, HTTPException, Path # depends is dependency injection
from starlette import status
import models
from models import Todos
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from routers import auth



app = FastAPI()
# create the database tables if not exists, this will run only when the database does not exist
models.Base.metadata.create_all(bind = engine)

app.include_router(auth.router) # include the router in the main application


# get db only when using it 
#created the db dependency
#this will create a session for each request and close it after the request is completed
#this is a dependency injection
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]

#create the pydantic request model for the todo, basemodel is part of pydantic library
class TodoRequest(BaseModel):
    title : str = Field(min_length = 3) 
    description : str = Field(min_length = 3 , max_length = 100)
    priority: int = Field(gt = 0, lt= 6)
    complete: bool



## end point to get the data in database
@app.get("/" , status_code = status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()



# endpoint to fetch the todo with the id
@app.get("/todo/{todo_id}", status_code = status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt = 0)): #path parameter validation 
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() # this to do will be fetched from the database
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code = 404, detail = "Todo not found")        



#endpoint to post and save the todo in the database
@app.post("/todo", status_code = status.HTTP_201_CREATED)
async def create_todo(db : db_dependency , todo_request : TodoRequest):
    todo_model = Todos(**todo_request.dict()) # unpacking the request model to the database model

    db.add(todo_model)
    db.commit()



#endpoint to update the todo in the database
@app.put("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id : int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = "Todo not found")
    

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


    
#endpoint to delete the todo from the database
@app.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = "Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()  # delete the todo from the databas
    db.commit()

