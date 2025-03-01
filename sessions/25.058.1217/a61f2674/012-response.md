# a61f2674 • 012 • refine_coder

---
```python
"""
1.  **Identify Center Line:** Locate the vertical line of gray (5) pixels in the center column of the input grid.
2.  **Recolor Center Line:** Change the color of this center line from gray (5) to blue (1) in the output grid, maintaining its position and length.
3.  **Locate Left Gray Pixels:** Identify the gray (5) pixels located to the left of the center line.
4.  **Create Red Lines:** For *each* of these identified gray pixels, create a red (2) vertical line in the output grid. This red line starts at the exact row and column of the gray pixel and extends downwards to the bottom edge of the grid.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds a vertical line of the specified color in the center column."""
    height, width = grid.shape
    center_column = width // 2
    line_indices = []
    for row in range(height):
        if grid[row, center_column] == color:
            line_indices.append((row, center_column))
    return line_indices

def find_pixels_left_of_line(grid, line_indices, color):
    """Finds pixels of a specific color to the left of a line."""
    left_pixels = []
    line_x = line_indices[0][1] if line_indices else -1 #get x coordinate of the line
    
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row,col] == color and col < line_x:
                left_pixels.append((row,col))
    return left_pixels

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Find the vertical gray line in the center
    gray_line_indices = find_vertical_line(input_grid, 5)

    # Replace the gray line with a blue line
    for row, col in gray_line_indices:
        output_grid[row, col] = 1

    # Find other gray pixels to the left
    left_gray_pixels = find_pixels_left_of_line(input_grid, gray_line_indices, 5)

    # Create red lines for each left gray pixel
    for gray_row, gray_col in left_gray_pixels:
        for row in range(gray_row, height):
            output_grid[row, gray_col] = 2

    return output_grid
```
