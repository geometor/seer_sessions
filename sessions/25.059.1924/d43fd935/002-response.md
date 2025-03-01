# d43fd935 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation extends blue (color 1) pixels to adjacent white cells when they meet a 2x2 green(3) block. Other object are unchanged.
"""

import numpy as np

def find_objects(grid):
    """Finds all non-zero colored objects and 2x2 green blocks in the grid."""
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                object_pixels = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    row, col = queue.pop(0)
                    object_pixels.append((row, col))

                    # Check adjacent cells (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < rows and 0 <= new_col < cols and \
                           grid[new_row, new_col] == color and not visited[new_row, new_col]:
                            queue.append((new_row, new_col))
                            visited[new_row, new_col] = True
                
                objects.append({'color': color, 'pixels': object_pixels})

    return objects

def is_2x2_green_block(obj, grid):
    """Checks if an object is a 2x2 green block."""

    if obj['color'] != 3:
      return False

    pixels = obj['pixels']
    if len(pixels) != 4:
        return False
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    if (max_row - min_row == 1) and (max_col - min_col == 1):
        return True

    return False
    

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = np.copy(grid)  # Initialize output_grid as a copy of input_grid

    objects = find_objects(grid)

    blue_pixel_exists = any(obj['color'] == 1 for obj in objects)
    green_2x2_block_exists = any(is_2x2_green_block(obj, grid) for obj in objects )

    # extend based on the condition
    if blue_pixel_exists and green_2x2_block_exists:
        for obj in objects:
          if is_2x2_green_block(obj, grid):
             for r,c in obj['pixels']:
                output_grid[r,c] = 1 # change 2x2 green to blue
          if obj['color'] == 1:
             for r, c in obj['pixels']:
                # Check adjacent cells (up, down, left, right) and change to 1
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_row, new_col = r + dr, c + dc
                    if 0 <= new_row < rows and 0 <= new_col < cols and output_grid[new_row,new_col] == 0 :
                        output_grid[new_row, new_col] = 1

    return output_grid.tolist()  # Convert back to list
```
