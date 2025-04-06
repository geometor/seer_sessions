
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

Okay, analyzing the provided examples to understand the transformation.

**Perception of Task Elements:**

*   **Input/Output:** Both are 3x3 grids containing single digits.
*   **Cells:** Each grid position holds a single digit.
*   **Values:** The digits seem to represent different states. '0' appears to be a background or empty state. Non-zero digits (2, 7, 8, 6, 4, 3) seem to represent filled states or objects.
*   **Transformation:** The change from input to output involves filling '0' cells based on the non-zero values above them within the same column. Non-zero values seem to propagate downwards, filling any '0' cells below them until they hit another non-zero value or the bottom of the grid.

**YAML Facts:**


```yaml
objects:
  - type: grid
    properties:
      size: 3x3
      cells:
        - type: cell
          properties:
            value: integer (0-9)
            position: [row, column]
  - type: number
    properties:
      value: integer (1-9)
      role: represents a filled state or object
  - type: zero
    properties:
      value: 0
      role: represents an empty state or background

relationships:
  - type: spatial
    description: Cells are arranged in rows and columns.
  - type: vertical_dependency
    description: The value of a '0' cell in the output depends on the non-zero values located directly above it in the same column in the input.

actions:
  - name: fill_downwards
    actor: non-zero number
    target: zero cells below in the same column
    effect: Changes the value of the target zero cells to the value of the actor non-zero number.
    condition: The cells between the actor and the target (inclusive) must all be zeros in the original input.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each column of the grid from left to right (column index `c` from 0 to 2).
3.  Within each column, iterate through the rows from top to bottom (row index `r` from 0 to 2).
4.  Maintain a variable `last_non_zero_value` for the current column, initialized to 0 before starting the row iteration for that column.
5.  For each cell `(r, c)`:
    *   If the value of the cell `(r, c)` in the *input* grid is non-zero, update `last_non_zero_value` to this value.
    *   If the value of the cell `(r, c)` in the *input* grid is zero *and* `last_non_zero_value` is not zero, set the value of the cell `(r, c)` in the *output* grid to `last_non_zero_value`.
6.  After processing all cells, the output grid contains the transformed result.
```python
import copy

"""
Fill '0' cells downwards within each column based on the nearest non-zero value above them.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each column of the grid.
3. Within each column, iterate through the rows from top to bottom.
4. Maintain the last seen non-zero value for the current column.
5. If the current cell in the input grid is non-zero, update the last seen non-zero value.
6. If the current cell in the input grid is zero and a non-zero value has been seen above it in the same column, set the corresponding cell in the output grid to the last seen non-zero value.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling zero cells downwards in each column
    with the value of the nearest non-zero cell above them in that column.
    """
    # Get grid dimensions
    if not input_grid:
        return []
    rows = len(input_grid)
    if rows == 0:
        return [[]]
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column
    for c in range(cols):
        # Keep track of the last non-zero value encountered in this column
        last_non_zero_value = 0
        # Iterate through each row in the current column
        for r in range(rows):
            # Check the value in the original input grid
            current_input_value = input_grid[r][c]

            if current_input_value != 0:
                # If the current cell is non-zero, update the last seen non-zero value
                last_non_zero_value = current_input_value
            elif last_non_zero_value != 0:
                # If the current cell is zero AND we have seen a non-zero value above it,
                # update the corresponding cell in the output grid
                output_grid[r][c] = last_non_zero_value

    # Return the transformed grid
    return output_grid

```
