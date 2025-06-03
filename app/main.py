from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, crud, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db 
    finally:
        db.close()    

@app.get("/")
def read_root():
    return{"message": "welcome to the To-Do list API"}


@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo noy found")
    return todo

@app.post('/todos')
def create_todo(title: str, description: str = "", db: Session = Depends(get_db)):
    return crud.create_todo(db, title, description)


@app.delete("/todos/todo_id")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not Found")
    return {"detail": "ToDo deleted successfully"}



