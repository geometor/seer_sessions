
## train_1

**input:**
```
7 1 7 8 0
0 8 7 7 1
7 7 7 7 7
8 7 7 7 1
0 1 7 8 5
```


**output:**
```
5 1 7 8 0
0 8 7 5 1
7 7 7 7 7
8 5 7 0 1
0 1 7 8 5
```


## train_2

**input:**
```
8 9 7 9 3
3 7 7 7 8
7 7 7 7 7
8 7 7 7 8
2 9 7 9 2
```


**output:**
```
8 9 7 9 3
3 2 7 2 8
7 7 7 7 7
8 3 7 3 8
2 9 7 9 2
```


## train_3

**input:**
```
7 4 7 4 5
4 3 7 7 3
7 7 7 7 7
5 7 7 4 3
3 4 7 5 7
```


**output:**
```
5 4 7 4 5
4 3 7 4 3
7 7 7 7 7
5 4 7 4 3
3 4 7 5 4
```

*   **Perception of Elements:**
    *   The input and output are 5x5 grids of single-digit integers.
    *   The transformation primarily affects cells containing the digit '7'.
    *   A central cross shape (row 2 and column 2, 0-indexed) seems significant. Cells within this cross, if they are '7', remain unchanged. All non-'7' cells also remain unchanged.
    *   The core transformation applies only to cells containing '7' that are *outside* the central cross.
    *   The transformation rule for these specific '7's appears related to rotational symmetry around the center of the grid (cell 2,2).
    *   The value of the symmetrically opposite cell `(4-r, 4-c)` plays a key role.
    *   There seems to be a base rule involving the symmetrical cell's value and a fallback rule when the symmetrical cell also contains '7'.
    *   The corner values of the input grid, specifically the bottom-left `I[4,0]` and top-right 
`I[0,4]`, seem involved in the fallback rule.

*   **YAML Facts:**
    
```yaml
    grid_dimensions: [5, 5]
    center_cell_coords: [2, 2] # 0-indexed
    marker_digit: 7
    invariant_cells:
      - type: central_cross # row 2 or column 2
      - type: non_marker_digit # cells not equal to 7
    target_cells:
      - type: marker_digit_outside_cross # cells equal to 7 AND r != 2 AND c != 2
    transformation_rule:
      depends_on:
        - target_cell_value: # Always 7
        - symmetrical_cell_value: input[4-r][4-c]
        - corner_values: [input[0,4], input[4,0]] # Top-right and Bottom-left
      relationship: Positional Symmetry and Conditional Value Assignment
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each cell `(r, c)` of the input grid (rows `r` from 0 to 4, columns `c` from 0 to 4).
    3.  Check if the current cell `(r, c)` contains the marker digit '7' AND is outside the central cross (i.e., `r` is not 2 AND `c` is not 2).
    4.  If the condition in step 3 is true:
        a.  Find the coordinates of the symmetrically opposite cell: `sr = 4 - r`, `sc = 4 - c`.
        b.  Get the value of the symmetrical cell from the *input* grid: `sym_val = input[sr][sc]`.
        c.  **Rule Application:**
            i.  If `sym_val` is NOT 7, update the output grid at `(r, c)` with `sym_val`: `output[r][c] = sym_val`.
            ii. If `sym_val` IS 7 (meaning both the cell and its symmetrical partner are '7's outside the cross), apply a fallback rule based on the cell's row position and specific corner values from the *input* grid:
                *   If the cell's row `r` is less than 2 (top half), update the output grid at `(r, c)` with the value from the bottom-left corner of the input grid: `output[r][c] = input[4][0]`.
                *   If the cell's row `r` is greater than 2 (bottom half), update the output grid at `(r, c)` with the value from the top-right corner of the input grid: `output[r][c] = input[0][4]`.
    5.  If the condition in step 3 is false (the cell is not '7' or is part of the central cross), the output cell value remains the same as the input cell value (already handled by initializing output as a copy of input).
    6.  Return the final output grid.
```python
"""
Transforms a 5x5 grid of integers based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (r, c) of the input grid.
3. Identify 'target' cells: cells containing the digit '7' that are outside the central cross (i.e., r != 2 and c != 2).
4. For each target cell:
    a. Find the symmetrically opposite cell coordinates (sr = 4 - r, sc = 4 - c).
    b. Get the value of the symmetrical cell from the *input* grid (sym_val = input[sr][sc]).
    c. If sym_val is NOT 7, update the output grid at (r, c) with sym_val.
    d. If sym_val IS 7 (fallback rule):
        i. If the target cell's row r is less than 2 (top half), update the output grid at (r, c) with the value from the input grid's bottom-left corner (input[4][0]).
        ii. If the target cell's row r is greater than 2 (bottom half), update the output grid at (r, c) with the value from the input grid's top-right corner (input[0][4]).
5. Cells that are not target cells (i.e., not '7' or are on the central cross) remain unchanged.
6. Return the final output grid.
"""

import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation rule to a 5x5 grid based on symmetrical cell values
    and corner values for specific '7' cells outside the central cross.
    """
    # Ensure the grid is 5x5, although the logic assumes this implicitly
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if rows != 5 or cols != 5:
        # Or raise an error, depending on desired behavior for invalid input size
        print("Warning: Input grid is not 5x5. Logic may not apply correctly.")
        # Attempt to proceed anyway, might fail if indices go out of bounds

    # Initialize output_grid as a deep copy of input_grid to avoid modifying the input
    # during symmetrical lookups.
    output_grid = copy.deepcopy(input_grid)

    # Define the marker digit and grid dimensions (0-indexed max)
    marker_digit = 7
    max_idx = 4 # for 5x5 grid

    # Retrieve corner values needed for the fallback rule
    bottom_left_corner_val = input_grid[max_idx][0]
    top_right_corner_val = input_grid[0][max_idx]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is a 'target' cell:
            # - Contains the marker digit (7)
            # - Is outside the central cross (row 2 and column 2)
            if input_grid[r][c] == marker_digit and r != 2 and c != 2:
                # Find the coordinates of the symmetrically opposite cell
                sr = max_idx - r
                sc = max_idx - c

                # Get the value of the symmetrical cell from the *input* grid
                sym_val = input_grid[sr][sc]

                # Apply the main transformation rule
                if sym_val != marker_digit:
                    output_grid[r][c] = sym_val
                # Apply the fallback rule if the symmetrical cell is also a marker digit
                else:
                    # Check if the target cell is in the top half (rows 0, 1)
                    if r < 2:
                        output_grid[r][c] = bottom_left_corner_val
                    # Check if the target cell is in the bottom half (rows 3, 4)
                    elif r > 2:
                         output_grid[r][c] = top_right_corner_val
                    # Note: The middle row (r=2) is excluded by the initial 'target cell' check,
                    # so we don't need an explicit condition for it here.

            # If the cell is not a target cell, its value remains unchanged
            # (already handled by the initial deep copy).

    return output_grid
```
