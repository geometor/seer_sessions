```python
import copy
import numpy as np

"""
Identifies the initial block of identical rows at the top of the input grid. 
Determines the set of 'target columns' - these are columns that contain at least one '8' within this top block.
Copies the input grid to create the output grid.
Iterates through the rows starting from the row immediately below the top block.
For each row in this lower section and for each 'target column', if the cell in the output grid is '0', it changes it to '8'. Existing non-zero values (like '2') are preserved.
"""

def find_last_top_row(grid: list[list[int]]) -> int:
    """
    Finds the index of the last row belonging to the initial block of identical top rows.

    Args:
        grid: The input grid.

    Returns:
        The index of the last row in the top block. Returns -1 if the grid is empty
        or 0 if there's only one row or the first two rows differ. Handles non-rectangular potential inputs during comparison.
    """
    if not grid:
        return -1
    if len(grid) == 1:
        return 0

    first_row = grid[0]
    last_top_row = 0
    # Iterate starting from the second row (index 1)
    for r in range(1, len(grid)):
        # Check if the current row is identical to the first row
        # Add a check for row length consistency
        if len(grid[r]) == len(first_row) and grid[r] == first_row:
            last_top_row = r
        else:
            # Stop when a different row is found
            break
    return last_top_row

def find_target_columns(grid: list[list[int]], last_top_row: int, target_value: int) -> set[int]:
    """
    Finds the indices of columns containing the target_value within the specified top rows.

    Args:
        grid: The input grid.
        last_top_row: The index of the last row to check (inclusive).
        target_value: The value to search for in the columns (e.g., 8).

    Returns:
        A set of column indices containing the target_value in the top block.
    """
    # Handle cases with empty grid or invalid last_top_row
    if not grid or last_top_row < 0 or not grid[0]:
        return set()

    num_cols = len(grid[0]) # Assume grid is rectangular based on examples
    target_columns = set()
    
    # Determine the number of rows to check in the top block
    rows_to_check = min(last_top_row + 1, len(grid))

    # Iterate through each column index
    for c in range(num_cols):
        # Check each row within the defined top block for the target value
        for r in range(rows_to_check):
             # Basic bounds check, although grid should be rectangular
            if c < len(grid[r]) and grid[r][c] == target_value:
                # If the target value is found in this column, add the column index to the set
                target_columns.add(c)
                # Once found in a column, no need to check further rows for this column
                break 
    return target_columns

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the identified rule.
    """
    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return []

    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(input_grid)
    # num_cols = len(input_grid[0]) # Assumes rectangular

    # --- Workflow ---

    # 1. Identify the block of identical rows at the top
    last_top_row = find_last_top_row(input_grid)

    # 2. Determine the columns that contain the value '8' within this top block
    target_columns = find_target_columns(input_grid, last_top_row, 8)

    # 3. Iterate through rows starting *below* the identified top block
    start_fill_row = last_top_row + 1
    for r in range(start_fill_row, num_rows):
        # For each of these rows, iterate through the target columns
        for c in target_columns:
             # Ensure column index is valid for the current row (for safety)
            if c < len(output_grid[r]):
                # If the cell in the current row and target column is '0', change it to '8'
                # This preserves any existing non-zero values (like '2')
                if output_grid[r][c] == 0:
                    output_grid[r][c] = 8

    # 4. Return the modified grid
    return output_grid
```