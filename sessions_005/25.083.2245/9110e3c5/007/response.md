```python
"""
Transforms an input grid into a 3x3 output grid containing only black (0) and azure (8) pixels. The arrangement of azure pixels is determined by the counts of specific colors in the input grid, forming either a horizontal line or an L-shape (regular or reversed).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with black (0) pixels
    output_grid = np.zeros((3, 3), dtype=int)

    # Count the occurrences of each color in the input grid
    color_counts = {}
    for color in range(10):
        color_counts[color] = np.count_nonzero(input_grid == color)

    # Determine the output pattern and azure count
    if color_counts[2] >= 12:
      # If count of color 2 >= 12: horizontal line of 3
      output_grid[1, 0] = 8
      output_grid[1, 1] = 8
      output_grid[1, 2] = 8

    elif color_counts[1] >= 4 and color_counts[2] < 12:
        # If the count of color 1 >= 4 and color 2 < 12: check for L-shape
        if color_counts[3] >= color_counts[1]:
            # standard L
            output_grid[0, 1] = 8
            output_grid[0, 2] = 8
            output_grid[1, 1] = 8
            output_grid[2, 1] = 8
        else:
            # reversed L
            output_grid[0, 2] = 8
            output_grid[1, 0] = 8
            output_grid[1, 1] = 8
            output_grid[2, 1] = 8

    elif color_counts[3] >= 4:
          output_grid[0, 1] = 8
          output_grid[0, 2] = 8
          output_grid[1, 1] = 8
          output_grid[2, 1] = 8
    else:
       # Otherwise output is horizontal line of 3
        output_grid[1, 0] = 8
        output_grid[1, 1] = 8
        output_grid[1, 2] = 8

    return output_grid
```