"""
Main entry point for the Todo Console Application.
This module contains the main application loop and integrates UI and operations.
"""
import sys
from typing import Optional

from .data import get_all_todos
from .ui import display_menu, get_user_choice, display_results, get_todo_input, get_todo_id_input
from .operations import add_todo, view_todos, mark_complete, update_todo, delete_todo


def main():
    """
    Main application loop that orchestrates the todo application.
    Integrates UI and operations modules with error handling.
    """
    print("Welcome to the Todo Console App!")

    while True:
        try:
            # Display menu and get user choice
            display_menu()
            choice = get_user_choice()

            if choice == 1:
                # Add Todo
                description = get_todo_input("Enter todo description: ")
                result = add_todo(description)
                display_results(result)

            elif choice == 2:
                # View Todos
                todos = view_todos()
                display_results(todos)

            elif choice == 3:
                # Mark Todo Complete
                all_todos = get_all_todos()
                if not all_todos:
                    print("No todos available to mark complete.")
                    continue

                todo_id = get_todo_id_input("Enter todo ID to mark complete: ")
                if todo_id is not None:
                    result = mark_complete(todo_id)
                    display_results(result)
                else:
                    print("Invalid ID entered.")

            elif choice == 4:
                # Update Todo
                all_todos = get_all_todos()
                if not all_todos:
                    print("No todos available to update.")
                    continue

                todo_id = get_todo_id_input("Enter todo ID to update: ")
                if todo_id is not None:
                    new_description = get_todo_input("Enter new description: ")
                    result = update_todo(todo_id, new_description)
                    display_results(result)
                else:
                    print("Invalid ID entered.")

            elif choice == 5:
                # Delete Todo
                all_todos = get_all_todos()
                if not all_todos:
                    print("No todos available to delete.")
                    continue

                todo_id = get_todo_id_input("Enter todo ID to delete: ")
                if todo_id is not None:
                    result = delete_todo(todo_id)
                    display_results(result)
                else:
                    print("Invalid ID entered.")

            elif choice == 6:
                # Exit
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose a number between 1-6.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again or contact support if the issue persists.")


if __name__ == "__main__":
    main()