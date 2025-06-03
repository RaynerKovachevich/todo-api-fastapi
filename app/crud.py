from sqlalchemy.orm import Session
from . import models

def get_all_todos(db: Session):
    return db.query(models.ToDo).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()

def create_todo(db: Session, title: str, description: str = ""):
    todo = models.ToDo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return todo