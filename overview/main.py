from fastapi import FastAPI, HTTPException
from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field



api = FastAPI()

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo")
    todo_description: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")


class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier of the todo")

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo")
    todo_description: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")



all_todo = [
    Todo(todo_id=1, todo_name="Buy groceries", todo_description="Milk, Bread, Eggs", priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name="Read a book", todo_description="Finish reading '1984'", priority=Priority.LOW),
    Todo(todo_id=3, todo_name="Workout", todo_description="Go for a 30-minute run", priority=Priority.HIGH),
    Todo(todo_id=4, todo_name="Call Mom", todo_description="Check in and see how she's doing", priority=Priority.HIGH),
    Todo(todo_id=5, todo_name="Clean the house", todo_description="Vacuum and dust all rooms", priority=Priority.MEDIUM),
]


@api.get("/todo", response_model=List[Todo])
def get_todo():
    return all_todo


@api.get("/todo/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    for todo in all_todo:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api.get("/todos")
def get_first_n_todos(first_n: int = None):
    if first_n and first_n > 0:
        return all_todo[:first_n]
    return all_todo

@api.post("/todo", response_model=Todo)
def add_todo(new_todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todo) + 1 if all_todo else 1
    
    new_todo = Todo(todo_id=new_todo_id, **new_todo.model_dump())
    all_todo.append(new_todo)
    return new_todo

@api.put("/todo/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for index, todo in enumerate(all_todo):
        if todo.todo_id == todo_id:
            updated_data = updated_todo.model_dump(exclude_unset=True)
            updated_todo_instance = todo.model_copy(update=updated_data)
            all_todo[index] = updated_todo_instance
            return updated_todo_instance   
    raise HTTPException(status_code=404, detail="Todo not found")

@api.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todo):
        if todo.todo_id == todo_id:
            deleted_todo = all_todo.pop(index)
            return {"Deleted": deleted_todo}
    raise HTTPException(status_code=404, detail="Todo not found")