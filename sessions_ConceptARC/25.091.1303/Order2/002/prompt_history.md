
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 4 4 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 6 0 0 6 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0
6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0
```

**Perception**

The task involves rearranging colored pixels within a grid based on a gravity-like principle. In both examples, the input grid contains colored pixels (yellow in train_1, magenta in train_2) scattered on a white background. The output grid shows these same colored pixels consolidated at the bottom of their respective columns. Each colored pixel appears to "fall" downwards within its column until it reaches the bottom edge of the grid or rests upon another colored pixel already settled in that column. The relative vertical order of the colored pixels within a single column seems to be preserved during this process. The background white pixels essentially act as empty space through which the colored pixels fall.

**Facts**


```yaml
objects:
  - type: pixel
    properties:
      color: integer (0-9)
      position: tuple (row, column)
      is_background: boolean (true if color is 0)
      is_colored: boolean (true if color is not 0)
actions:
  - name: fall_down
    target: colored_pixel
    constraints:
      - moves_within_same_column
      - stops_at_grid_bottom
      - stops_at_another_colored_pixel_below
relationships:
  - type: spatial
    description: Pixels exist within a 2D grid structure.
  - type: column_constraint
    description: Movement (falling) is restricted to the pixel's original column.
  - type: stacking
    description: Falling pixels stack vertically upon other pixels or the grid bottom within the same column.
  - type: order_preservation
    description: The relative vertical order of colored pixels within a column is maintained after falling.
```


**Natural Language Program**

1.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
2.  Process the input grid column by column, from left to right.
3.  For each column:
    a.  Identify all the colored (non-white) pixels within that column.
    b.  Collect the colors of these pixels in a list, maintaining their top-to-bottom order as found in the input grid column.
    c.  Starting from the bottom row of the output grid and moving upwards within the current column, place the collected colored pixels from the list (in their original relative order) into the available cells.
4.  The resulting grid, after processing all columns, is the final output.
```python
"""
Applies a gravity-like transformation to a 2D grid. Colored pixels (non-zero)
in each column "fall" downwards, stacking at the bottom of the column or on top
of other fallen pixels within the same column, while maintaining their original
relative vertical order. The background pixels (zero) are treated as empty space.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by applying gravity to colored pixels within each column.

    Args:
        input_grid (list of lists or np.ndarray): The input 2D grid.

    Returns:
        np.ndarray: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    num_rows, num_cols = grid.shape

    # Initialize output_grid with the same dimensions as input_grid, filled with background color (0)
    output_grid = np.zeros_like(grid)

    # Process each column independently
    for c in range(num_cols):
        # Extract the current column
        column = grid[:, c]

        # Find the colored pixels (non-zero values) in this column
        colored_pixels = column[column != 0]

        # Determine the number of colored pixels
        num_colored = len(colored_pixels)

        # Place the colored pixels at the bottom of the corresponding column in the output_grid
        if num_colored > 0:
            # The starting row index in the output grid for placing the first colored pixel
            start_row = num_rows - num_colored
            # Assign the collected colored pixels to the bottom part of the output column
            output_grid[start_row:num_rows, c] = colored_pixels

    return output_grid.tolist() # Return as list of lists per spec
```
