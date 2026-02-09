from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List


from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)   # As soon as we start the application there will be a posts table in the database

app = FastAPI()


try:
    conn = psycopg2.connect(host = 'localhost', database = 'FastApi', user = 'postgres', password = 'Santosh@2005', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DataBase Connection Successful.")
except Exception as e:
    print("Connection Failed to DataBase")
    print("Error:", e)
    time.sleep(2)



# my_posts = [
#     {
#         "title": "What happens to request",
#         "content": "Nothing it gets accepted",
#         "published": "true",
#         "rating": 8.1,
#         "id": 1
#     },
#     {
#         "title": "What happens to server",
#         "content": "Nothing actually...",
#         "published": "true",
#         "rating": 7.9,
#         "id": 2
#     }
# ]

@app.get("/")
def root():
    return {
        "message": "Welcome Social"
    }

# @app.get("/sqlal")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": posts}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return posts



@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    #using .all() will make the db search for the post with id even after finding it so using first() will just return the post which it found at first
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(f""" INSERT INTO posts (title, content, published) VALUES ({post.title, post.content, post.published})""") Vulnarable to SQL Injections
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrive the new post
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", str(id,))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found..."
        )
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return {
        "status": "success"
    }

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found..."
        )
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 