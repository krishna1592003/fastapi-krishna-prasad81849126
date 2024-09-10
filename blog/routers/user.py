from fastapi import APIRouter ,Depends,status , HTTPException
from typing import List 
from .. import schemas , database ,models 
from sqlalchemy.orm import Session 
from ..Hashing import Hash 


router = APIRouter(
     prefix='/user',
    tags = ['user']
   

)

get_db = database.get_db





@router.post('/' , response_model=schemas.ShowUser )
def create_user( request:schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name= request.name, email= request.email,password= Hash.bcrypt(request.password)) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.ShowUser)
def ShowUserdata(id:int, db:Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id ).first() 
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the {id} is not available")
    return user_data