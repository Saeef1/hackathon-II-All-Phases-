# Data Model: Todo In-Memory Python Console App

## Todo Entity

### Attributes
- **id** (integer): Unique identifier for the todo item; auto-generated sequentially
- **description** (string): Text description of the task; required field
- **completed** (boolean): Completion status of the task; defaults to False
- **created_at** (datetime): Timestamp when the todo was created; auto-generated

### Relationships
- The Todo entity exists independently with no direct relationships to other entities
- All Todo instances are stored in a single in-memory list structure

## Data Structure

### In-Memory Storage
- **todos_list**: A Python list containing all Todo entities as dictionaries
- Each dictionary has the structure: `{'id': int, 'description': str, 'completed': bool, 'created_at': datetime}`
- The list maintains insertion order
- IDs are generated sequentially starting from 1

### Validation Rules
- **description**: Must be a non-empty string (length > 0)
- **completed**: Must be a boolean value (True/False)
- **id**: Must be unique within the list and positive integer
- **created_at**: Automatically set to current timestamp when created

## State Transitions

### Todo Lifecycle
1. **Created**: New todo with `completed=False` and current timestamp
2. **Active**: Todo exists in the list, available for viewing, updating, or completion
3. **Completed**: Todo marked as `completed=True`
4. **Deleted**: Todo removed from the list (final state)

## Operations Impact on Data

### Add Operation
- Creates new Todo dictionary with provided description
- Sets `completed=False` by default
- Generates next available ID
- Appends to `todos_list`

### Update Operation
- Modifies the `description` field of existing Todo dictionary
- Preserves all other attributes unchanged

### Mark Complete Operation
- Changes `completed` field to `True` for specified Todo
- Preserves all other attributes unchanged

### Delete Operation
- Removes Todo dictionary from `todos_list`
- ID becomes available for potential reuse (though not actively reused)

## Constraints

### Business Rules
- No two todos can have the same ID at the same time
- Description cannot be empty
- Todos cannot be "uncompleted" once marked complete (one-way transition)
- IDs are never reused within the same application session

### Technical Constraints
- Data exists only in memory during application runtime
- No persistence mechanism implemented
- Maximum practical todo count limited by available memory