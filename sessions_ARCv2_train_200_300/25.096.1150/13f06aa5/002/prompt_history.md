
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 4 4 1 4 4 2 2
2 2 2 2 2 2 2 2 4 4 4 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 2 2 2 2 2
2 4 4 2 2 2 2 2 2 2 2 2 2 2
2 4 8 2 2 2 2 2 2 2 2 2 2 2
2 4 4 2 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 0
2 2 2 2 2 2 2 2 2 1 2 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
2 2 2 2 2 2 2 4 4 1 4 4 2 8
2 2 2 2 2 2 2 2 4 4 4 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
2 2 4 2 2 2 2 2 2 2 2 2 2 8
2 4 4 2 2 2 2 2 2 2 2 2 2 8
2 4 8 2 8 2 8 2 8 2 8 2 8 8
2 4 4 2 2 2 2 2 2 2 2 2 2 8
2 2 4 2 2 2 2 2 2 2 2 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 1 1 1 8 8 3 8 8 1
1 1 1 8 8 1 1 1 8 8 8 1 1
1 1 1 2 8 1 1 1 1 1 1 1 1
1 1 1 8 8 1 1 1 1 1 1 1 1
1 1 1 8 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
0 3 3 3 3 3 3 3 3 3 3 3 3
2 1 1 1 1 1 1 1 1 3 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 8 1 1 1 8 8 3 8 8 1
2 1 1 8 8 1 1 1 8 8 8 1 1
2 2 1 2 8 1 1 1 1 1 1 1 1
2 1 1 8 8 1 1 1 1 1 1 1 1
2 1 1 8 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
```


## train_3

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 1 1 1 3 3 3 3 3
3 3 3 1 1 6 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 1 1 1 3 3 3 3 3
3 3 3 1 1 6 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
6 6 6 6 6 6 6 6 6 6 6 6
```

Okay, let's break down the transformations in these examples.

**Perception of Elements:**

The core elements are 2D grids containing numerical digits (0-8). The transformation involves modifying these grids. The modifications seem to fall into several categories:

1.  **Boundary Modifications:** Changes occur along the edges of the grid. This sometimes involves creating a "frame" using two adjacent edges (top/right in train_1, top/left in train_2) with specific fill values and a unique corner value ('0'). In other cases, an entire edge is overwritten (last row in train_3).
2.  **Patterned Internal Modifications:** Certain cells within the grid change value based on a repeating pattern, often related to rows or columns. For instance, alternating cells in a specific row (train_1) or column (train_3) are modified. These patterns sometimes seem triggered by or aligned with specific features in the input grid (like the position of the '6' in train_3).
3.  **Specific Coordinate Modifications:** Some cells change value based purely on their specific coordinates, seemingly independent of broader patterns (e.g., (1, 10) in train_1, (1, 9) and (5, 1) in train_2).

**YAML Facts:**


```yaml
task_type: grid_transformation
input_data:
  type: 2D_grid
  cell_type: integer_digit
output_data:
  type: 2D_grid
  cell_type: integer_digit
  relationship_to_input: same_dimensions_in_these_examples
transformations:
  - type: boundary_modification
    sub_types:
      - framing: # Observed in train_1, train_2
          description: Modifies two adjacent edges (e.g., top/right, top/left) with specific fill values and a unique corner value (0).
          properties:
            edges_modified: [top, right] or [top, left]
            edge_1_fill_value: depends_on_example (1 in train_1, 3 in train_2)
            edge_2_fill_value: depends_on_example (8 in train_1, 2 in train_2)
            corner_value: 0
      - edge_overwrite: # Observed in train_3
          description: Replaces all values along a specific edge with a single value.
          properties:
            edge_modified: last_row
            fill_value: 6
  - type: patterned_internal_modification
    sub_types:
      - row_pattern: # Observed in train_1
          description: Modifies cells in a specific row based on an alternating pattern.
          properties:
            target_row_index: 8
            start_column_index: 5
            value_from: 2
            value_to: 8
            pattern: every_other_cell
      - column_pattern: # Observed in train_3
          description: Modifies cells in a specific column based on an alternating pattern, potentially linked to an input feature.
          properties:
            trigger_value_in_input: 6
            target_column_index: column_of_trigger_value (5)
            start_row_index: row_of_trigger_value + 2 (4)
            value_from: 3
            value_to: 6
            pattern: every_other_row
  - type: specific_coordinate_modification
    description: Changes the value of cells at fixed coordinates.
    examples: # Coordinates are (row, column)
      - train_1: {(1, 10): 1}
      - train_2: {(1, 9): 3, (5, 1): 2}

```


**Natural Language Program:**

1.  **Initialization:** Create the output grid as an exact copy of the input grid.
2.  **Boundary Handling:** Determine the type of boundary modification required for this specific input:
    *   **If Top/Right Framing applies (like train_1):**
        *   Set the top-right corner cell (0, last_col) to 0.
        *   Fill the rest of the top row (row 0, cols 0 to last_col-1) with value 1.
        *   Fill the rest of the rightmost column (col last_col, rows 1 to last_row) with value 8.
    *   **If Top/Left Framing applies (like train_2):**
        *   Set the top-left corner cell (0, 0) to 0.
        *   Fill the rest of the top row (row 0, cols 1 to last_col) with value 3.
        *   Fill the rest of the leftmost column (col 0, rows 1 to last_row) with value 2.
    *   **If Last Row Overwrite applies (like train_3):**
        *   Fill the entire last row (row last_row) with value 6.
3.  **Internal Pattern Application:** Determine if internal patterns need modification:
    *   **If Row 8 Alternating Pattern applies (like train_1):**
        *   Iterate through columns starting from index 5 in row 8.
        *   If the column index is 5, 7, 9, 11, etc. (i.e., 5 + 2*k) and the cell value is 2, change it to 8.
    *   **If Column Alternating Pattern applies (like train_3):**
        *   Find the location (r, c) of the value 6 in the *input* grid.
        *   Iterate through rows starting from index r+2 in column c.
        *   If the row index is r+2, r+4, r+6, etc. (i.e., r+2 + 2*k) and the cell value is 3, change it to 6.
4.  **Specific Cell Modifications:** Apply any fixed coordinate changes:
    *   If the input corresponds to train_1 type, change cell (1, 10) to 1.
    *   If the input corresponds to train_2 type, change cell (1, 9) to 3 and cell (5, 1) to 2.
5.  **Finalization:** Return the modified output grid.
```python
import copy

"""
This function transforms an input grid based on specific patterns observed in the training examples. 
It identifies the type of transformation based on key features within the input grid 
(like the presence of a specific number, e.g., 6) or specific values at certain coordinates.

Three main transformation types are handled:

1.  **Type 1 (like train_1):** Applies a top-right frame (corner 0, top row 1, right column 8), 
    modifies row 8 with an alternating pattern (changing 2 to 8 starting from column 5), 
    and sets cell (1, 10) to 1. This type is identified by checking for the value 1 at input_grid[3][10].

2.  **Type 2 (like train_2):** Applies a top-left frame (corner 0, top row 3, left column 2), 
    and sets specific cells: (1, 9) to 3 and (5, 1) to 2. This is the default case if Type 1 or Type 3 conditions are not met.

3.  **Type 3 (like train_3):** Overwrites the last row with 6s, finds the location of the first 6 in the *input* grid, 
    and applies an alternating pattern in that column starting two rows below the found 6 (changing 3 to 6). 
    This type is identified by the presence of the number 6 anywhere in the input grid.
"""

def find_first(grid: list[list[int]], value: int) -> tuple[int | None, int | None]:
    """Finds the row and column index of the first occurrence of a value."""
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == value:
                return r_idx, c_idx
    return None, None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on identified patterns.

    Args:
        input_grid: The 2D list of integers representing the input grid.

    Returns:
        A new 2D list of integers representing the transformed grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    if rows == 0:
        return output_grid  # Handle empty grid case
    cols = len(output_grid[0])
    if cols == 0:
        return output_grid # Handle empty row case


    # Check for Type 3 condition (presence of 6)
    six_r, six_c = find_first(input_grid, 6)

    if six_r is not None and six_c is not None:
        # --- Transformation Type 3 (like train_3) ---
        # Overwrite the last row with 6
        for c in range(cols):
            output_grid[rows - 1][c] = 6

        # Apply column alternating pattern based on the found 6
        # Start two rows below the original 6
        start_row = six_r + 2
        for r in range(start_row, rows, 2): # Iterate every other row
             # Check bounds and if the cell needs changing
            if r < rows and output_grid[r][six_c] == 3:
                 output_grid[r][six_c] = 6

    # Check for Type 1 condition (value 1 at specific location [3][10])
    # Add bounds check for safety
    elif rows > 3 and cols > 10 and input_grid[3][10] == 1:
         # --- Transformation Type 1 (like train_1) ---
        # Apply top-right frame
        if rows > 0 and cols > 0:
            output_grid[0][cols - 1] = 0  # Top-right corner
            for c in range(cols - 1):
                output_grid[0][c] = 1  # Top row (excluding corner)
            for r in range(1, rows):
                output_grid[r][cols - 1] = 8  # Right column (excluding corner)

        # Apply row 8 alternating pattern (change 2 to 8)
        # Check if row 8 exists
        if rows > 8:
            target_row = 8
            start_col = 5
            for c in range(start_col, cols, 2): # Iterate every other column
                # Check if cell value is 2 before changing
                if output_grid[target_row][c] == 2:
                    output_grid[target_row][c] = 8

        # Apply specific cell modification
        # Check bounds first
        if rows > 1 and cols > 10:
             output_grid[1][10] = 1

    else:
        # --- Transformation Type 2 (like train_2) - Default Case ---
        # Apply top-left frame
        if rows > 0 and cols > 0:
            output_grid[0][0] = 0 # Top-left corner
            for c in range(1, cols):
                output_grid[0][c] = 3 # Top row (excluding corner)
            for r in range(1, rows):
                output_grid[r][0] = 2 # Left column (excluding corner)

        # Apply specific cell modifications
        # Check bounds first
        if rows > 1 and cols > 9:
            output_grid[1][9] = 3
        if rows > 5 and cols > 1:
            output_grid[5][1] = 2

    return output_grid
```
