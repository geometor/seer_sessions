# 4612dd53 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a blue shape in the input grid and adds/changes red pixels adjacent to it. The red pixels seem to trace the inside and outside outline of the blue shape.
"""

import numpy as np

def find_blue_shape(grid):
    """Finds the contiguous region of blue pixels."""
    blue_pixels = np.argwhere(grid == 1)
    if len(blue_pixels) == 0:
        return []

    # Simple contiguous region finding (may need refinement for complex shapes)
    shape = []
    
    # start with one, then keep adding neighbors until no more
    shape.append(tuple(blue_pixels[0]))
    
    added = True
    while added:
      added = False
      for bp in blue_pixels:
        bptuple = tuple(bp)
        if bptuple not in shape:
          for s in shape:
            if (abs(bp[0] - s[0]) <= 1 and abs(bp[1] - s[1]) == 0) or \
               (abs(bp[1] - s[1]) <= 1 and abs(bp[0] - s[0]) == 0):
              shape.append(bptuple)
              added = True
              break    
    return shape

def get_neighbors(grid, pixel):
    """Returns the neighbors (up, down, left, right) of a pixel."""
    rows, cols = grid.shape
    r, c = pixel
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)
    blue_shape = find_blue_shape(grid)

    # Iterate through blue shape pixels and their neighbors
    for pixel in blue_shape:
      
        neighbors = get_neighbors(grid, pixel)
        for neighbor in neighbors:
            # if a white pixel touches the blue shape, consider for change
            if grid[neighbor] == 0:
              output_grid[neighbor] = 2
            # if a blue pixel touches another blue pixel, consider for change
            if grid[neighbor] == 1:
              output_grid[pixel] = 2  # change blue to red based on some condition

    return output_grid.tolist()
```
