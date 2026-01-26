"""
Data module for the Todo Console Application.
Contains the Todo entity and in-memory storage.
"""
from datetime import datetime
from typing import Dict, List, Optional


class Todo:
    """
    Represents a single todo item with id, description, completion status, and creation timestamp.
    """
    def __init__(self, todo_id: int, description: str, completed: bool = False):
        self.id = todo_id
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert the Todo object to a dictionary representation."""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

    def __str__(self) -> str:
        """String representation of the Todo item."""
        status = 'x' if self.completed else ' '
        return f"[{self.id}] [{status}] {self.description}"


# Global in-memory storage for todos
todos_list: List[Todo] = []
next_id: int = 1


def get_next_id() -> int:
    """Generate the next available ID for a new todo."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id


def add_todo_to_storage(description: str) -> Todo:
    """Add a new todo to the in-memory storage."""
    global todos_list
    todo_id = get_next_id()
    new_todo = Todo(todo_id, description)
    todos_list.append(new_todo)
    return new_todo


def get_all_todos() -> List[Todo]:
    """Retrieve all todos from storage."""
    return todos_list


def get_todo_by_id(todo_id: int) -> Optional[Todo]:
    """Retrieve a specific todo by its ID."""
    for todo in todos_list:
        if todo.id == todo_id:
            return todo
    return None


def update_todo_description(todo_id: int, new_description: str) -> bool:
    """Update the description of an existing todo."""
    todo = get_todo_by_id(todo_id)
    if todo:
        todo.description = new_description
        return True
    return False


def mark_todo_completed(todo_id: int) -> bool:
    """Mark a todo as completed."""
    todo = get_todo_by_id(todo_id)
    if todo and not todo.completed:
        todo.completed = True
        return True
    return False


def delete_todo_by_id(todo_id: int) -> bool:
    """Remove a todo from storage by its ID."""
    global todos_list
    original_length = len(todos_list)
    todos_list = [todo for todo in todos_list if todo.id != todo_id]
    return len(todos_list) < original_length


def clear_all_todos():
    """Clear all todos from storage (used for resetting)."""
    global todos_list, next_id
    todos_list = []
    next_id = 1