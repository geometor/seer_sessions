# 4be741c5 • 018 • refine_coder

---
```python
"""
Identifies nested squares within the input grid and extracts the color of the
innermost square's center pixel to create a 1x1 output grid.
"""

import numpy as np

def get_center_pixel(grid):
    """Returns the color of the center pixel of a grid."""
    rows = len(grid)
    cols = len(grid[0])
    return grid[rows // 2][cols // 2]

def find_innermost_square(grid):
    """
    Recursively finds the innermost square in a grid.

    Args:
      grid: The input grid (list of lists).

    Returns:
       The innermost square (list of lists).
    """
    rows = len(grid)
    cols = len(grid[0])

    # Base case: If the grid is 1x1, it's the innermost square.
    if rows == 1 and cols == 1:
        return grid

    # Find the outermost color.
    outer_color = grid[0][0]

    # Check if the grid is a solid square of the same color
    is_solid_square = True
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != outer_color:
                is_solid_square = False
                break
        if not is_solid_square:
            break
    
    if is_solid_square: return grid


    # Extract the inner grid by removing the outer border.
    inner_grid = [row[1:-1] for row in grid[1:-1]]
    
    if not inner_grid or not inner_grid[0]:
       return grid
        
    # Recursively find the innermost square in the inner grid.
    return find_innermost_square(inner_grid)

def transform(input_grid):
    """
    Transforms the input grid to extract the color of the central pixel of the
    innermost nested square, and output is a 1 x 1 grid with that value.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list: A 1x1 grid (list of lists) containing the color of the innermost
              square's center pixel.
    """
    # Find the innermost square.
    innermost_square = find_innermost_square(input_grid)

    # Get the color of the center pixel of the innermost square.
    center_color = get_center_pixel(innermost_square)

    # Create a 1x1 output grid with the center color.
    output_grid = np.array([[center_color]])

    return output_grid.tolist()
```
