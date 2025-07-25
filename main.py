from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Todo as TodoModel
import models


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


class Todo(BaseModel):
    title:str
    completed:bool


app = FastAPI()

@app.get('/todos')
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.post('/todos')
def create_todos(todo: Todo, db: Session = Depends(get_db)):
    db_todo = TodoModel(
        title=todo.title,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


  
@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not db_todo:
        return {"error": "Todo not found"}

    db_todo.title = todo.title
    db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo

  # DELETE - obriši todo
@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    if not db_todo:
        return {"error": "Todo not found"}

    db.delete(db_todo)
    db.commit()

    return {"message": "Todo deleted", "todo": db_todo}

