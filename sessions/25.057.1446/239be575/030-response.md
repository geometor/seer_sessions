# 239be575 • 030 • refine_coder

---
```python
"""
The output grid is a 1x1 grid. The color of the output grid's single pixel is determined by the color of the outer perimeter of the input grid.
"""

import numpy as np

def get_perimeter_color(grid):
    # Get the shape of the input grid
    rows, cols = grid.shape
    # Create sets to store unique colors for the entire perimeter and corners
    perimeter_colors = set()
    corner_colors = set()

    # Add corner colors to both sets
    corner_colors.add(grid[0, 0])
    perimeter_colors.add(grid[0, 0])
    corner_colors.add(grid[0, cols - 1])
    perimeter_colors.add(grid[0, cols - 1])
    corner_colors.add(grid[rows - 1, 0])
    perimeter_colors.add(grid[rows - 1, 0])
    corner_colors.add(grid[rows - 1, cols - 1])
    perimeter_colors.add(grid[rows - 1, cols - 1])

    # Add colors from the top and bottom rows (excluding corners, already added)
    for j in range(1, cols - 1):
        perimeter_colors.add(grid[0, j])
        perimeter_colors.add(grid[rows - 1, j])

    # Add colors from the left and right columns (excluding corners, already added)
    for i in range(1, rows - 1):
        perimeter_colors.add(grid[i, 0])
        perimeter_colors.add(grid[i, cols - 1])
    
    # If all colors in the set a the same, return that color
    if len(perimeter_colors) == 1:
      return perimeter_colors.pop()
    else:
      # if more than one color in perimeter, something went wrong
      return None


def transform(input_grid):
    # Get the perimeter color.
    perimeter_color = get_perimeter_color(input_grid)

    # Initialize the output grid as a 1x1 array with the perimeter color.
    output_grid = np.array([[perimeter_color]])

    return output_grid
```
