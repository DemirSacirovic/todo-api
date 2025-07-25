from fastapi import FastAPI
from pydantic import BaseModel



class Todo(BaseModel):
    title:str
    completed:bool

todos_db = []
todo_counter = 1


app = FastAPI()

@app.get('/todos')
def get_all_todos():
    return todos_db


@app.post('/todos')
def create_todos(todo:Todo):
    global todo_counter
    new_item = {'id' : todo_counter, 'title' : todo.title, 'completed' : todo.completed}
    todos_db.append(new_item)    
    todo_counter +=1
    return new_item

@app.put('/todos/{todo_id}')
def update_todo(todo_id : int, todo : Todo):
    for i in range(len(todos_db)):
        if todos_db[i]['id'] == todo_id:
            todos_db[i] = {'id':todo_id, 'title' : todo.title, 'completed' : todo.completed}
            return todos_db[i]
    return {'error': 'Todo not found'}

@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for i in range(len(todos_db)):
        if todos_db[i]['id'] == todo_id:
            deleted = todos_db.pop(i)  # Briše i vraća
            return {"message": "Deleted", "item": deleted}
    return {"error": "Todo not found"}
