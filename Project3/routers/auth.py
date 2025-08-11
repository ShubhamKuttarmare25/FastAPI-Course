from fastapi import APIRouter  

router = APIRouter()


#this is a diffent api application and need to run this separately
#this is handle with the help of router 

@router.get("/auth")
async def get_user():
    return {'user': 'autheticated'} 
