"""
Utility functions for validation and error handling in the Todo Console Application.
"""


def validate_todo_description(description: str) -> tuple[bool, str]:
    """
    Validate a todo description.

    Args:
        description: The description to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not description or not description.strip():
        return False, "Todo description cannot be empty"

    if len(description.strip()) == 0:
        return False, "Todo description cannot be empty"

    # Check for reasonable length (optional validation)
    if len(description) > 500:  # Reasonable limit for a todo description
        return False, "Todo description is too long (max 500 characters)"

    return True, ""


def validate_todo_id(todo_id: int, todos_list: list) -> tuple[bool, str]:
    """
    Validate that a todo ID exists in the current list.

    Args:
        todo_id: The ID to validate
        todos_list: The list of existing todos

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(todo_id, int) or todo_id <= 0:
        return False, "Todo ID must be a positive integer"

    # Check if the ID exists in the list
    for todo in todos_list:
        if todo.id == todo_id:
            return True, ""

    return False, f"Todo with ID {todo_id} does not exist"


def safe_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Safely get integer input from user with validation.

    Args:
        prompt: The prompt to display to the user
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)

    Returns:
        The validated integer value, or None if invalid input
    """
    try:
        value = int(input(prompt))
        if min_val is not None and value < min_val:
            return None
        if max_val is not None and value > max_val:
            return None
        return value
    except ValueError:
        return None


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class TodoNotFoundError(Exception):
    """Exception raised when a todo is not found."""
    pass