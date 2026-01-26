"""
UI module for the Todo Console Application.
Handles all user interface interactions.
"""
from typing import List, Union, Dict, Optional

from .utils import safe_int_input


def display_menu():
    """
    Show available options to user.
    """
    print("\n" + "="*40)
    print("Todo Console App")
    print("="*40)
    print("1. Add Todo")
    print("2. View Todos")
    print("3. Mark Todo Complete")
    print("4. Update Todo")
    print("5. Delete Todo")
    print("6. Exit")
    print("="*40)


def get_user_choice() -> int:
    """
    Gets and validates user menu selection.

    Returns:
        The selected menu option (1-6), or -1 if invalid input
    """
    choice = safe_int_input("Choose an option (1-6): ", min_val=1, max_val=6)
    return choice if choice is not None else -1


def get_todo_input(prompt: str) -> str:
    """
    Gets todo description from user.

    Args:
        prompt: The prompt to display

    Returns:
        The user input string
    """
    return input(prompt)


def get_todo_id_input(prompt: str) -> Optional[int]:
    """
    Gets todo ID from user.

    Args:
        prompt: The prompt to display

    Returns:
        The user input integer ID or None if invalid
    """
    return safe_int_input(prompt)


def display_results(results: Union[Dict, str, List]):
    """
    Formats and displays operation results to the user.

    Args:
        results: The results to display
    """
    if isinstance(results, dict):
        # Handle operation results
        if results.get("success"):
            message = results.get("message", "")
            if message:
                print(message)

            # Display todos if available in the result
            todos = results.get("todos")
            if todos is not None:
                if len(todos) == 0:
                    print("No todos to display.")
                else:
                    print("Todos:")
                    for todo in todos:
                        status = 'x' if todo['completed'] else ' '
                        print(f"  [{todo['id']}] [{status}] {todo['description']}")

            # Display single todo if available
            todo = results.get("todo")
            if todo:
                status = 'x' if todo['completed'] else ' '
                print(f"  [{todo['id']}] [{status}] {todo['description']}")
        else:
            # Display error message
            error_msg = results.get("message", "Unknown error occurred")
            print(f"Error: {error_msg}")
    elif isinstance(results, str):
        print(results)
    elif isinstance(results, list):
        if len(results) == 0:
            print("No items to display.")
        else:
            print("Items:")
            for item in results:
                if isinstance(item, dict) and 'id' in item and 'description' in item:
                    status = 'x' if item.get('completed', False) else ' '
                    print(f"  [{item['id']}] [{status}] {item['description']}")
                else:
                    print(f"  {item}")
    else:
        print(f"Result: {results}")