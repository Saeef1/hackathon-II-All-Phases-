# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13+ installed on your system
- Basic familiarity with command-line/console applications

## Setup Instructions

1. Clone or download the repository containing the todo application
2. Navigate to the application directory in your terminal/console
3. Ensure Python 3.13+ is available by running:
   ```bash
   python --version
   ```

## Running the Application

1. Execute the main application file:
   ```bash
   python main.py
   ```

2. The application will start and display the main menu with available options

## Using the Application

### Main Menu Options

Once the application starts, you'll see a menu with the following options:

1. **Add Todo** - Create a new todo item
   - Select option 1
   - Enter your todo description when prompted
   - Press Enter to confirm

2. **View Todos** - Display all existing todo items
   - Select option 2
   - All todos will be displayed with their completion status

3. **Mark Todo Complete** - Mark a specific todo as completed
   - Select option 3
   - Enter the ID of the todo you want to mark complete
   - The todo's status will be updated

4. **Update Todo** - Modify the description of an existing todo
   - Select option 4
   - Enter the ID of the todo you want to update
   - Enter the new description
   - The todo's description will be updated

5. **Delete Todo** - Remove a specific todo from the list
   - Select option 5
   - Enter the ID of the todo you want to delete
   - The todo will be removed from the list

6. **Exit** - Quit the application
   - Select option 6
   - The application will close (note: all data will be lost as it's in-memory only)

### Example Usage Session

```
Welcome to the Todo Console App!
1. Add Todo
2. View Todos
3. Mark Todo Complete
4. Update Todo
5. Delete Todo
6. Exit

Choose an option: 1
Enter todo description: Buy groceries
Todo added successfully!

Choose an option: 2
Todos:
[1] [ ] Buy groceries

Choose an option: 3
Enter todo ID to mark complete: 1
Todo marked as complete!

Choose an option: 2
Todos:
[1] [x] Buy groceries

Choose an option: 6
Goodbye!
```

## Important Notes

- All data is stored in-memory only and will be lost when the application exits
- Todo IDs are automatically assigned sequentially starting from 1
- Completed todos will show an [x] next to their ID
- Incomplete todos will show an [ ] next to their ID
- Invalid inputs will be handled gracefully with error messages

## Troubleshooting

- If the application fails to start, ensure Python 3.13+ is installed and accessible
- If options don't work, ensure you're entering valid numeric IDs that exist in the list
- If you encounter an error, restart the application (remember data is not persisted)