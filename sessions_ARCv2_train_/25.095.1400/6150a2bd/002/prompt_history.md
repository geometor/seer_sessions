
## train_1

**input:**
```
5 5 2
1 0 0
0 0 0
```


**output:**
```
0 0 0
0 0 1
2 5 5
```


## train_2

**input:**
```
3 3 8
3 7 0
5 0 0
```


**output:**
```
0 0 5
0 7 3
8 3 3
```

**Perception:**

The input and output are both 2D grids (or matrices) of integers. In both provided examples, the input grid seems to undergo a spatial transformation to produce the output grid. The numbers themselves within the grid are preserved, but their positions change. Comparing the input and output grids side-by-side, the transformation appears consistent with a 180-degree rotation. The element at the top-left corner of the input moves to the bottom-right corner of the output, the element at the top-right moves to the bottom-left, and so on, effectively reversing both row and column order.

**Facts:**


```yaml
Input:
  type: Grid
  data_type: integer
  dimensions: 3x3 (based on examples)
Output:
  type: Grid
  data_type: integer
  dimensions: 3x3 (based on examples)
Transformation:
  type: Spatial Rotation
  details: 180-degree rotation
  preserves_values: true
  changes_positions: true
Relationships:
  - Output grid element at row `r`, column `c` corresponds to the input grid element at row `max_row - 1 - r`, column `max_col - 1 - c`.
  - The set of numerical values present in the input grid is identical to the set of numerical values in the output grid.
```


**Natural Language Program:**

1.  Read the input grid.
2.  Create a new output grid with the same dimensions as the input grid.
3.  Iterate through each cell `(r, c)` of the input grid, where `r` is the row index and `c` is the column index.
4.  Determine the dimensions of the input grid (let `num_rows` be the number of rows and `num_cols` be the number of columns).
5.  Place the value from the input grid cell `(r, c)` into the output grid cell at position `(num_rows - 1 - r, num_cols - 1 - c)`.
6.  Return the completed output grid.
```python
"""
Transforms an input grid by rotating it 180 degrees. The value at input cell (r, c) 
is moved to output cell (num_rows - 1 - r, num_cols - 1 - c).
"""

import copy # Although not strictly necessary for this implementation, 
            # it's good practice if modifications were made in place.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid: A list of lists representing the input 2D integer grid.

    Returns:
        A list of lists representing the 180-degree rotated output grid.
    """
    # Determine the dimensions of the input grid
    if not input_grid:
        return [] # Handle empty input grid
    num_rows = len(input_grid)
    if num_rows == 0 or not input_grid[0]:
         # Handle grid with zero rows or zero columns
        return [[] for _ in range(num_rows)] 
    num_cols = len(input_grid[0])

    # Initialize the output grid with the same dimensions, filled with a placeholder (e.g., 0)
    # Using list comprehension for concise initialization
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Calculate the corresponding position in the output grid after 180-degree rotation
            output_row = num_rows - 1 - r
            output_col = num_cols - 1 - c

            # Place the value from the input grid into the calculated output grid position
            output_grid[output_row][output_col] = input_grid[r][c]

    # Return the completed output grid
    return output_grid
```
