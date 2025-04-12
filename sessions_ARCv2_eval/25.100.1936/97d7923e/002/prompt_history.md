
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 7 0 0 0 0 0 0 0 5 0 0 0 0
0 0 7 0 0 1 0 0 0 0 5 0 0 3 0
0 0 7 0 0 7 0 1 0 0 5 0 0 5 0
0 0 7 0 0 7 0 7 0 0 5 0 0 5 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```


**output:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 1 0 0 0 0 0 0 0 5 0 0 0 0
0 0 1 0 0 1 0 0 0 0 5 0 0 3 0
0 0 1 0 0 7 0 1 0 0 5 0 0 3 0
0 0 1 0 0 7 0 7 0 0 5 0 0 3 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids (matrices) containing non-negative integers. The dimensions (rows and columns) of the grid remain unchanged.
2.  **Values:** The grids contain mostly zeros, with some non-zero digits scattered throughout.
3.  **Transformation Scope:** Changes seem localized within individual columns. One column's transformation doesn't appear to affect other columns directly.
4.  **Nature of Change:** Specific non-zero values within a column are being replaced by another non-zero value from the same column. Zeros remain zeros.
5.  **Trigger Condition:** The change seems triggered by the *minimum* non-zero value present in a column.
6.  **Positional Dependence:** The change applies only to cells *below* the first occurrence of this minimum non-zero value within the column. Values above or at the same row as the first minimum non-zero value are unaffected.
7.  **Target Value:** The non-zero values below the trigger row are changed *to* the minimum non-zero value identified for that column.

**Facts (YAML):**


```yaml
Task: Grid Transformation by Column Propagation

Objects:
  - Grid:
      Properties:
        - rows: Integer (number of rows)
        - columns: Integer (number of columns)
        - cells: List of Lists (holding cell values)
  - Column:
      Properties:
        - index: Integer
        - values: List of Integers (values in that column)
      Derived Properties:
        - non_zero_values: List of Integers
        - min_non_zero_value: Integer (smallest value > 0 in the column, if any)
        - first_min_row_index: Integer (row index of the first occurrence of min_non_zero_value, if any)
  - Cell:
      Properties:
        - row: Integer
        - column: Integer
        - value: Integer

Relationships:
  - A Grid contains multiple Columns and Cells.
  - A Column contains multiple Cells (one per row).
  - A transformation rule is applied independently to each Column.

Actions:
  - Iterate through each Column of the input Grid.
  - Identify non-zero values within the current Column.
  - If multiple non-zero values exist:
      - Find the minimum non-zero value (`min_val`) for the Column.
      - Find the row index (`trigger_row`) of the first occurrence of `min_val`.
      - Iterate through rows below `trigger_row`.
      - Modify Cell values: For cells in the current Column below `trigger_row`, if their value is non-zero, change it to `min_val`.
  - Copy unchanged Cell values to the output Grid.
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid.
2.  Process the grid column by column, from left to right.
3.  For each column:
    a.  Identify all non-zero values present in that column and note their row indices.
    b.  If there are fewer than two non-zero values in the column, copy the entire column from the input to the output grid and proceed to the next column.
    c.  If there are two or more non-zero values:
        i.  Find the minimum value among the non-zero values identified in step 3a. Call this `min_val`.
        ii. Find the lowest row index where `min_val` appears in this column. Call this `trigger_row`.
        iii. Copy the values from the input column to the output column for all rows up to and including `trigger_row`.
        iv. For each row *below* `trigger_row`:
            1. Check the value in the input grid at this row and the current column.
            2. If the value is non-zero, set the corresponding cell in the output grid to `min_val`.
            3. If the value is zero, set the corresponding cell in the output grid to zero.
4.  Return the completed output grid.
```python
import copy

"""
Processes a 2D grid of integers column by column. 
For each column:
1. Finds all non-zero values.
2. If fewer than two non-zero values exist, the column remains unchanged.
3. If two or more non-zero values exist:
   a. Identifies the minimum non-zero value (`min_val`) in the column.
   b. Finds the row index (`trigger_row`) of the *first* occurrence of `min_val`.
   c. For all rows *below* `trigger_row`, any non-zero value in that column is replaced with `min_val`. 
   d. Values at or above `trigger_row`, and all zero values, remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the column-based transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    # This ensures unchanged cells/columns are correctly preserved
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column index
    for c_idx in range(num_cols):
        # --- Find non-zero elements and their locations in the current column ---
        non_zero_info = [] # List to store tuples of (value, row_index)
        for r_idx in range(num_rows):
            value = input_grid[r_idx][c_idx]
            if value != 0:
                non_zero_info.append((value, r_idx))

        # --- Check if transformation is needed (at least two non-zeros) ---
        if len(non_zero_info) < 2:
            # If less than 2 non-zeros, this column remains unchanged (already copied)
            continue

        # --- Determine the minimum non-zero value ---
        # Extract just the values from non_zero_info
        non_zero_values = [val for val, r_idx in non_zero_info]
        min_val = min(non_zero_values)

        # --- Find the first row index where the minimum value occurs ---
        trigger_row = -1 # Initialize trigger_row
        for val, r_idx in non_zero_info:
            if val == min_val:
                trigger_row = r_idx
                break # Stop at the first occurrence

        # Ensure trigger_row was found (should always happen if len >= 2)
        if trigger_row == -1: 
             # This case should technically not be reached if len(non_zero_info) >= 2
             # but included for robustness
             continue

        # --- Apply the transformation to rows below the trigger row ---
        # Iterate through rows starting from the one *after* the trigger row
        for r_idx in range(trigger_row + 1, num_rows):
            # Check if the *original* value at this position was non-zero
            if input_grid[r_idx][c_idx] != 0:
                # If it was non-zero, update the corresponding cell in the output grid
                output_grid[r_idx][c_idx] = min_val
            # If the original value was zero, it remains zero (already copied)

    # Return the modified grid
    return output_grid
```
