from fastapi import APIRouter ,Depends,status , HTTPException
from typing import List 
from .. import schemas , database ,models ,Oauth
from sqlalchemy.orm import Session 



router = APIRouter(
    prefix = '/blog',
    tags = ['blogs']

)

get_db = database.get_db

@router.get('/' , response_model=List[schemas.ShowBlog] )
def all(db :Session = Depends(get_db) , current_user: schemas.User = Depends(Oauth.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs 


@router.post('/' )
def create(request: schemas.Blog, db :Session = Depends(get_db),current_user: schemas.User = Depends(Oauth.get_current_user)): 
    new_blog = models.Blog(title = request.title , body = request.body, )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog 


@router.get('/{id}', status_code=status.HTTP_404_NOT_FOUND,response_model= schemas.ShowBlog, tags = ['blogs'])
def show(id,db :Session = Depends(get_db), current_user: schemas.User = Depends(Oauth.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
    
    return blog  




@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags = ['blogs'])
def destroy(id , db :Session = Depends(get_db), current_user: schemas.User = Depends(Oauth.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id )
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'
   

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED, tags = ['blogs'])
def update(id, request: schemas.Blog , db :Session = Depends(get_db),current_user: schemas.User = Depends(Oauth.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first()  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
    
    blog.update(request.dict())
    db.commit()
    return 'updated'