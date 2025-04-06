
## train_1

**input:**
```
0 2 0
7 0 8
0 0 0
```


**output:**
```
0 2 0
7 2 8
7 2 8
```


## train_2

**input:**
```
0 0 6
0 4 0
3 0 0
```


**output:**
```
0 0 6
0 4 6
3 4 6
```


## train_3

**input:**
```
4 0 0
0 2 0
0 0 0
```


**output:**
```
4 0 0
4 2 0
4 2 0
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

*   The input and output are grids of the same dimensions (3x3 in the examples).
*   The grids contain single-digit integers. The digit '0' appears to function as a background or empty space.
*   Non-zero digits (colors) seem to "fall" or propagate downwards within their columns.
*   If a cell contains '0' and the cell directly above it contains a non-zero digit, the '0' is replaced by that non-zero digit.
*   This downward propagation continues until the bottom of the grid is reached or another non-zero digit is encountered in the same column below the original propagating digit.
*   The process occurs independently for each column.

**YAML Facts:**


```yaml
objects:
  - name: grid
    type: 2D array of integers
    properties:
      - dimensions (rows, columns)
  - name: cell
    type: element within the grid
    properties:
      - position (row, column)
      - value (integer)
  - name: color
    type: non-zero integer value in a cell
  - name: background
    type: zero integer value in a cell

relationships:
  - type: spatial
    description: Cells are arranged in rows and columns. Each cell (except top row) has a cell directly above it in the same column.
  - type: state_change
    description: The value of a background cell can change based on the value of the cell above it.

actions:
  - name: propagate_downward
    actor: color
    target: background cell
    condition: The background cell is below the color cell in the same column, and all intermediate cells (if any) are also background cells.
    effect: The background cell's value changes to the color's value.
    scope: Occurs independently within each column.

grid_properties:
  - input and output grids have the same dimensions.
  - transformation modifies cell values based on column-wise rules.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each column of the grid independently, from left to right.
3.  For the current column, keep track of the most recently encountered non-zero value ('last_color'), initialized to 0 (background).
4.  Iterate through the rows of the current column from top (row 0) to bottom.
5.  For the current cell at `(row, column)`:
    *   If the cell's value in the input grid is non-zero, update `last_color` to this value.
    *   If the cell's value in the input grid is zero and `last_color` is non-zero, set the value of the corresponding cell in the output grid to `last_color`.
    *   If the cell's value in the input grid is zero and `last_color` is also zero, the cell in the output grid remains zero.
6.  After processing all columns, the output grid contains the transformed result.
```python
import copy

"""
Transforms a grid by propagating non-zero values downwards within each column. 
If a cell contains 0 (background) and the cell directly above it (or any cell further up in the same column, with only 0s in between) contains a non-zero value, the 0 is replaced by that non-zero value. This process repeats downwards within each column independently.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies downward propagation of non-zero values in each column of the grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Ensure input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # We modify this grid based on the input grid's state
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column independently
    for col_idx in range(num_cols):
        # Keep track of the last non-zero color encountered in this column
        last_color = 0
        # Iterate through each row in the current column from top to bottom
        for row_idx in range(num_rows):
            # Get the value from the *original* input grid for decision making
            current_input_value = input_grid[row_idx][col_idx]

            # If the current cell in the input grid has a non-zero value (a color)
            if current_input_value != 0:
                # Update the last seen color for this column
                last_color = current_input_value
                # The output grid already has this value from the deepcopy
            # If the current cell in the input grid is zero (background)
            # AND we have seen a non-zero color above it in this column
            elif current_input_value == 0 and last_color != 0:
                # Set the corresponding cell in the output grid to the last seen color
                output_grid[row_idx][col_idx] = last_color
            # If the current cell is 0 and last_color is also 0 (start of column or only 0s above)
            # The output grid cell remains 0 (already set by deepcopy)

    # Return the modified grid
    return output_grid
```
