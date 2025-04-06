
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

Okay, I will analyze the provided examples and extract the transformation logic.

## Perception of Task Elements

The input and output are square grids (3x3 in the examples) containing single-digit integers. The transformation modifies the grid based on the values and positions of the non-zero elements. Zeros ('0') appear to be placeholder values that can be replaced. Non-zero numbers seem to propagate downwards within their respective columns.

## Facts


```yaml
task_type: grid_transformation
grid_properties:
  - type: 2D array of integers
  - size: constant (3x3 in examples)
  - cell_values: integers (0-9 observed)
objects:
  - name: grid_cell
    properties:
      - value: integer
      - row_index: integer
      - column_index: integer
      - is_zero: boolean
  - name: grid_column
    properties:
      - index: integer
      - cells: ordered list of grid_cells
relationships:
  - type: spatial
    description: Cells are arranged in rows and columns.
  - type: vertical_dependency
    description: The value of a cell can be determined by the value of the cell(s) above it in the same column.
actions:
  - name: propagate_downward
    actor: non-zero_cell_value
    target: zero_cell_value
    condition: The zero cell is below the non-zero cell within the same column.
    effect: The zero cell's value is replaced by the most recent non-zero value encountered above it in that column.
transformation_focus: column-based processing
goal: Fill vertical gaps (zeros) below non-zero numbers within each column.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through each column of the grid independently, from left to right (column index `c` from 0 to width-1).
3.  For the current column `c`, initialize a variable `last_non_zero_value` to 0.
4.  Iterate through the rows of the current column `c`, from top to bottom (row index `r` from 0 to height-1).
5.  Examine the value of the cell at `(r, c)` in the *input* grid.
6.  If the input cell value is non-zero, update `last_non_zero_value` to this value.
7.  If the input cell value is zero *and* `last_non_zero_value` is non-zero, set the value of the corresponding cell `(r, c)` in the *output* grid to `last_non_zero_value`.
8.  If the input cell value is non-zero, ensure the corresponding cell `(r, c)` in the *output* grid also holds this non-zero value (it should already from the initial copy, but this clarifies the logic).
9.  After processing all rows for the current column, move to the next column.
10. Once all columns have been processed, the output grid contains the final transformed result.
```python
"""
Transforms an input grid by propagating the last seen non-zero value downwards within each column. 
Zeros below a non-zero number in a column are replaced by that number until another non-zero number is encountered in that column.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the downward propagation transformation to the input grid.

    Args:
        input_grid: A 2D list representing the input grid of integers.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Ensure the input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures original non-zero values are preserved unless overwritten
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column
    for c in range(width):
        # Initialize the last non-zero value seen in this column
        last_non_zero_value = 0

        # Iterate through each row within the current column, from top to bottom
        for r in range(height):
            # Get the value from the original input grid for reference
            input_value = input_grid[r][c]

            # If the input value is non-zero, update the last seen non-zero value
            if input_value != 0:
                last_non_zero_value = input_value
                # Ensure the output grid has this non-zero value (already true from copy, but explicit)
                output_grid[r][c] = input_value
            # If the input value is zero AND we have previously seen a non-zero value in this column
            elif last_non_zero_value != 0:
                # Update the corresponding cell in the output grid with the last non-zero value
                output_grid[r][c] = last_non_zero_value
            # If the input value is zero and no non-zero value has been seen yet in this column,
            # the output remains zero (as initialized by the copy).

    # Return the fully transformed grid
    return output_grid

```
