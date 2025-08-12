from fastapi import APIRouter, HTTPException, Path   
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, timezone, datetime





router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

# Secret key
SECRET_KEY = "dfd0aedf65609b606d83641d4b391dad67975a84b7527d9a7ef1b5586ed62d5d"
ALGORITHM = "HS256"  # Algorithm used for encoding the JWT



# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated= 'auto')

# OAuth2 password bearer token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")




# create the pydantic request model for the user, basemodel is part of pydantic library
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str



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
    return user  # return the user object if authentication is successful



#funtion to create a access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta ):

    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'username': username, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")







#this is a diffent api application and need to run this separately
#this is handle with the help of router 

@router.post("/", status_code = status.HTTP_201_CREATED)
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
@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = autheticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes = 20))
    return {'access_token': token, 'token_type': 'bearer'}  # this is just a placeholder, in real application we will validate the user and return the access token



