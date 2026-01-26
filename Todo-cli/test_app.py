"""
Simple test script to verify the Todo Console Application functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data import clear_all_todos, get_all_todos
from src.operations import add_todo, view_todos, mark_complete, update_todo, delete_todo


def test_add_todo():
    """Test adding a new todo."""
    print("Testing Add Todo functionality...")

    # Clear any existing todos
    clear_all_todos()

    # Add a new todo
    result = add_todo("Test todo item")
    print(f"Add result: {result}")

    # Verify the todo was added
    todos_result = view_todos()
    print(f"View result: {todos_result}")

    assert result["success"] == True, "Add todo should succeed"
    assert len(get_all_todos()) == 1, "There should be 1 todo after adding"

    print("OK Add Todo functionality works correctly\n")


def test_view_todos():
    """Test viewing todos."""
    print("Testing View Todos functionality...")

    # Clear and add a couple of todos
    clear_all_todos()
    add_todo("First todo")
    add_todo("Second todo")

    # View todos
    result = view_todos()
    print(f"View result: {result}")

    assert result["success"] == True, "View todos should succeed"
    assert len(result["todos"]) == 2, "There should be 2 todos"

    print("OK View Todos functionality works correctly\n")


def test_mark_complete():
    """Test marking a todo as complete."""
    print("Testing Mark Complete functionality...")

    # Clear and add a todo
    clear_all_todos()
    add_todo("Todo to complete")

    # Mark the first todo as complete
    result = mark_complete(1)
    print(f"Mark complete result: {result}")

    assert result["success"] == True, "Mark complete should succeed"

    # Verify the todo is marked as complete
    view_result = view_todos()
    todo = view_result["todos"][0]
    assert todo["completed"] == True, "Todo should be marked as completed"

    print("OK Mark Complete functionality works correctly\n")


def test_update_todo():
    """Test updating a todo."""
    print("Testing Update Todo functionality...")

    # Clear and add a todo
    clear_all_todos()
    add_todo("Old description")

    # Update the todo
    result = update_todo(1, "New description")
    print(f"Update result: {result}")

    assert result["success"] == True, "Update todo should succeed"

    # Verify the description was updated
    view_result = view_todos()
    todo = view_result["todos"][0]
    assert todo["description"] == "New description", "Todo description should be updated"

    print("OK Update Todo functionality works correctly\n")


def test_delete_todo():
    """Test deleting a todo."""
    print("Testing Delete Todo functionality...")

    # Clear and add a couple of todos
    clear_all_todos()
    add_todo("First todo")
    add_todo("Second todo")

    # Verify we have 2 todos
    initial_count = len(get_all_todos())
    assert initial_count == 2, "There should be 2 todos initially"

    # Delete the first todo
    result = delete_todo(1)
    print(f"Delete result: {result}")

    assert result["success"] == True, "Delete todo should succeed"

    # Verify we have 1 todo left
    final_count = len(get_all_todos())
    assert final_count == 1, "There should be 1 todo after deletion"

    print("OK Delete Todo functionality works correctly\n")


def run_all_tests():
    """Run all tests."""
    print("Starting Todo Console Application tests...\n")

    test_add_todo()
    test_view_todos()
    test_mark_complete()
    test_update_todo()
    test_delete_todo()

    print("SUCCESS: All tests passed! The Todo Console Application is working correctly.")


if __name__ == "__main__":
    run_all_tests()