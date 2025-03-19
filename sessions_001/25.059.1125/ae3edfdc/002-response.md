# ae3edfdc • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule identifies distinct colored objects in the input grid and replaces them with a "+" shaped object of the same color in the output grid. The "+" is centered at the approximate center of the original object. The background (color 0) remains unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous non-zero colored objects in the grid.
    Returns a list of objects, where each object is a dictionary containing:
        - color: The color of the object.
        - pixels: A list of (row, col) tuples representing the object's pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, pixels):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        dfs(row + 1, col, color, pixels)
        dfs(row - 1, col, color, pixels)
        dfs(row, col + 1, color, pixels)
        dfs(row, col - 1, color, pixels)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                objects.append({'color': color, 'pixels': pixels})
    return objects

def calculate_center(pixels):
    """
    Calculates the approximate center of a set of pixels.
    """
    if not pixels:
        return None
    row_sum = sum(p[0] for p in pixels)
    col_sum = sum(p[1] for p in pixels)
    return (round(row_sum / len(pixels)), round(col_sum / len(pixels)))

def create_plus_shape(center, color, output_grid):
    """
    Creates a "+" shaped object in the output grid.
    """
    row, col = center
    if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
      output_grid[row, col] = color
    if 0 <= row - 1 < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
      output_grid[row - 1, col] = color  # Up
    if 0 <= row + 1 < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
      output_grid[row + 1, col] = color  # Down
    if 0 <= row < output_grid.shape[0] and 0 <= col - 1 < output_grid.shape[1]:
      output_grid[row, col - 1] = color  # Left
    if 0 <= row < output_grid.shape[0] and 0 <= col + 1 < output_grid.shape[1]:
      output_grid[row, col + 1] = color  # Right

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find objects in the input grid
    objects = find_objects(input_grid)

    # for each object in input
    for obj in objects:
        # calculate center of mass
        center = calculate_center(obj['pixels'])
        # replace input pixels in output with '+' at center
        create_plus_shape(center, obj['color'], output_grid)
        
    return output_grid
```
