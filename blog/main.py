from fastapi import FastAPI, Depends ,status , HTTPException
from .import schemas,models
from .database import engine ,SessionLocal, get_db
from sqlalchemy.orm import Session 
from .Hashing import Hash 
from .routers import blog,user,authentication 
app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(authentication .router)
app.include_router(blog.router)
app.include_router(user.router)
 
#@app.post('/blog' , tags = ['blogs'])
#def create(request: schemas.Blog, db :Session = Depends(get_db)): 
#    new_blog = models.Blog(title = request.title , body = request.body, )
 #   db.add(new_blog)
 #   db.commit()
#    db.refresh(new_blog)
 #   return new_blog 



#getting the required data filtered by id 
#@app.get('/blog/{id}', status_code=status.HTTP_404_NOT_FOUND,response_model= schemas.ShowBlog, tags = ['blogs'])
#def show(id,db :Session = Depends(get_db)):
#    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#   if not blog :
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
#    return blog  




#@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags = ['blogs'])
'''def destroy(id , db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id )
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'
   

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags = ['blogs'])
def update(id, request: schemas.Blog , db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first()  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the {id} is not available")
    
    blog.update(request.dict())
    db.commit()
    return 'updated'

 




#@app.get('/blog' , response_model=List[schemas.ShowBlog], tags = ['blogs'])
#def all(db :Session = Depends(get_db)):
 #   blogs = db.query(models.Blog).all()
  
  #  return blogs 

@app.post('/user' , response_model=schemas.ShowUser ,tags = ['User'])
def create_user( request:schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name= request.name, email= request.email,password= Hash.bcrypt(request.password)) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}',response_model=schemas.ShowUser , tags = ['User'])
def ShowUserdata(id:int, db:Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id ).first() 
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the {id} is not available")
    return user_data
''' 
