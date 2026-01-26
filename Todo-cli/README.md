# Todo Console Application

A simple console-based todo application with in-memory storage, built with Python.

## Features

- Add new todo items
- View all todo items with their completion status
- Mark todo items as complete
- Update todo item descriptions
- Delete todo items

## Requirements

- Python 3.13 or higher

## Installation

1. Clone the repository
2. Install dependencies: `pip install -e .` (from the project root)

## Usage

Run the application:
```bash
python -m src.main
```

Or if installed as a package:
```bash
todo-app
```

## Example Session

```
Welcome to the Todo Console App!
========================================
Todo Console App
========================================
1. Add Todo
2. View Todos
3. Mark Todo Complete
4. Update Todo
5. Delete Todo
6. Exit
========================================
Choose an option (1-6): 1
Enter todo description: Buy groceries
Todo 'Buy groceries' added successfully!

Choose an option (1-6): 2
Found 1 todo(s).
Todos:
  [1] [ ] Buy groceries

Choose an option (1-6): 3
Enter todo ID to mark complete: 1
Todo with ID 1 marked as complete!

Choose an option (1-6): 2
Found 1 todo(s).
Todos:
  [1] [x] Buy groceries

Choose an option (1-6): 6
Goodbye!
```