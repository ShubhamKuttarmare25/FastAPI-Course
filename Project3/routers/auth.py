from fastapi import APIRouter  
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm





router = APIRouter()
# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated= 'auto')



# create the pydantic request model for the user, basemodel is part of pydantic library
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str



def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]


#wriiten to authenticate the user
def autheticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


#this is a diffent api application and need to run this separately
#this is handle with the help of router 

@router.post("/auth", status_code = status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request : CreateUserRequest):
    create_user_model = Users( # we cannot use (**create_user_request.dict()) here because it will not work with pydantic model as we have hashed_password
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),  # in real application we will hash the password
        is_active = True  # by default we will set the user as active
    )
    
    db.add(create_user_model)
    db.commit()  # commit the changes to the database


    #return create_user_model  # in real application we will save this to the database




#post request with path
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = autheticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'  # in real application we will raise HTTPException with 401 status code
    return 'Successfull Authentication'  # this is just a placeholder, in real application we will validate the user and return the access token

