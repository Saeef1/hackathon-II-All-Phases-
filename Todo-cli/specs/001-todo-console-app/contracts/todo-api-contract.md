# Todo API Contract: Console Application Interface

## Overview
This contract defines the interface between the user and the console-based todo application. Since this is a console application without traditional API endpoints, the contract describes the user interaction patterns and expected responses.

## User Actions & Expected Behaviors

### 1. Add Todo Operation
**Action**: User selects option 1 and provides a description
**Input**: String description of the todo (non-empty)
**Expected Response**:
- Success: Confirmation message "Todo added successfully!" and new todo appears in list
- Error: Error message if description is empty

### 2. View Todos Operation
**Action**: User selects option 2
**Input**: None
**Expected Response**:
- Success: Formatted list of all todos showing ID, completion status, and description
- Empty case: Message indicating no todos exist

### 3. Mark Todo Complete Operation
**Action**: User selects option 3 and provides a valid todo ID
**Input**: Integer ID of existing todo
**Expected Response**:
- Success: Confirmation message "Todo marked as complete!"
- Error: Error message if ID doesn't exist

### 4. Update Todo Operation
**Action**: User selects option 4 and provides a valid todo ID and new description
**Input**: Integer ID of existing todo and new string description
**Expected Response**:
- Success: Confirmation message "Todo updated successfully!"
- Error: Error message if ID doesn't exist or description is empty

### 5. Delete Todo Operation
**Action**: User selects option 5 and provides a valid todo ID
**Input**: Integer ID of existing todo
**Expected Response**:
- Success: Confirmation message "Todo deleted successfully!" and todo removed from list
- Error: Error message if ID doesn't exist

### 6. Exit Operation
**Action**: User selects option 6
**Input**: None
**Expected Response**:
- Success: Goodbye message and application termination

## Data Format Specifications

### Todo Representation
```
{
  "id": integer,
  "description": string,
  "completed": boolean,
  "created_at": datetime_string
}
```

### Console Display Format
```
[ID] [Status] Description
Where:
- ID: Sequential integer starting from 1
- Status: [ ] for incomplete, [x] for complete
- Description: User-provided text
```

## Error Handling Contract

### Error Messages Format
```
"Error: [Specific error description]"
```

### Expected Error Scenarios
1. Invalid menu selection → "Error: Please enter a valid option number"
2. Empty todo description → "Error: Todo description cannot be empty"
3. Non-existent todo ID → "Error: Todo with ID [X] does not exist"
4. Invalid ID format → "Error: Please enter a valid integer ID"

## Validation Rules
1. Todo descriptions must be non-empty strings
2. Todo IDs must be positive integers that exist in the current list
3. Menu selections must be integers between 1 and 6
4. All operations must preserve data integrity

## State Management
1. Todos persist in-memory during application session
2. Application state resets when application exits
3. IDs are assigned sequentially and not reused within a session
4. Completion status is irreversible (completed todos remain completed)