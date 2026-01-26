"""
Operations module for the Todo Console Application.
Contains all business logic functions for todo operations.
"""
from typing import Dict, List, Union

from .data import (
    add_todo_to_storage, get_all_todos, get_todo_by_id,
    update_todo_description, mark_todo_completed, delete_todo_by_id
)
from .utils import validate_todo_description, validate_todo_id, ValidationError, TodoNotFoundError


def add_todo(description: str) -> Dict[str, Union[str, bool]]:
    """
    Add a new todo to the list.

    Args:
        description: Description of the todo

    Returns:
        Result dictionary with success status and message
    """
    try:
        is_valid, error_msg = validate_todo_description(description)
        if not is_valid:
            return {"success": False, "message": error_msg}

        new_todo = add_todo_to_storage(description.strip())
        return {
            "success": True,
            "message": f"Todo '{new_todo.description}' added successfully!",
            "todo": new_todo.to_dict()
        }
    except Exception as e:
        return {"success": False, "message": f"Error adding todo: {str(e)}"}


def view_todos() -> Dict[str, Union[List[Dict], str, bool]]:
    """
    Return formatted list of all todos.

    Returns:
        Result dictionary with todos list and status
    """
    try:
        todos = get_all_todos()
        todos_dicts = [todo.to_dict() for todo in todos]

        if not todos:
            return {
                "success": True,
                "message": "No todos available.",
                "todos": []
            }

        return {
            "success": True,
            "message": f"Found {len(todos)} todo(s).",
            "todos": todos_dicts
        }
    except Exception as e:
        return {"success": False, "message": f"Error viewing todos: {str(e)}", "todos": []}


def mark_complete(todo_id: int) -> Dict[str, Union[str, bool]]:
    """
    Mark a todo as completed.

    Args:
        todo_id: ID of the todo to mark complete

    Returns:
        Result dictionary with success status and message
    """
    try:
        # Validate that the todo exists
        todos = get_all_todos()
        is_valid, error_msg = validate_todo_id(todo_id, todos)
        if not is_valid:
            return {"success": False, "message": error_msg}

        success = mark_todo_completed(todo_id)
        if success:
            return {
                "success": True,
                "message": f"Todo with ID {todo_id} marked as complete!"
            }
        else:
            return {
                "success": False,
                "message": f"Todo with ID {todo_id} was already completed."
            }
    except Exception as e:
        return {"success": False, "message": f"Error marking todo as complete: {str(e)}"}


def update_todo(todo_id: int, new_description: str) -> Dict[str, Union[str, bool]]:
    """
    Update todo description.

    Args:
        todo_id: ID of the todo to update
        new_description: New description for the todo

    Returns:
        Result dictionary with success status and message
    """
    try:
        # Validate that the todo exists
        todos = get_all_todos()
        is_valid, error_msg = validate_todo_id(todo_id, todos)
        if not is_valid:
            return {"success": False, "message": error_msg}

        # Validate the new description
        is_valid, error_msg = validate_todo_description(new_description)
        if not is_valid:
            return {"success": False, "message": error_msg}

        success = update_todo_description(todo_id, new_description.strip())
        if success:
            return {
                "success": True,
                "message": f"Todo with ID {todo_id} updated successfully!"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update todo with ID {todo_id}."
            }
    except Exception as e:
        return {"success": False, "message": f"Error updating todo: {str(e)}"}


def delete_todo(todo_id: int) -> Dict[str, Union[str, bool]]:
    """
    Remove a todo from the list.

    Args:
        todo_id: ID of the todo to delete

    Returns:
        Result dictionary with success status and message
    """
    try:
        # Validate that the todo exists
        todos = get_all_todos()
        is_valid, error_msg = validate_todo_id(todo_id, todos)
        if not is_valid:
            return {"success": False, "message": error_msg}

        success = delete_todo_by_id(todo_id)
        if success:
            return {
                "success": True,
                "message": f"Todo with ID {todo_id} deleted successfully!"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to delete todo with ID {todo_id}."
            }
    except Exception as e:
        return {"success": False, "message": f"Error deleting todo: {str(e)}"}