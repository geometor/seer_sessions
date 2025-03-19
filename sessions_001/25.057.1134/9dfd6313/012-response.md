# 9dfd6313 • 012 • refine_coder

---
```python
"""
The transformation identifies vertical objects of uniform color and reconstructs them horizontally. If we consider each input grid, we can observe:
1. Find vertical objects: identify contiguous vertical lines of non-zero pixels of the same color.
2. Reconstruct horizontally: For each object found, reconstruct it as a horizontal line in the output grid. The horizontal line's length should be equal to the original vertical object's height.  The y-coordinate (row) of the horizontal line in the output grid is determined by the original vertical object's row and height.

"""

import numpy as np

def find_vertical_objects(grid):
    """
    Identifies vertical objects (contiguous vertical lines of the same color) in a grid.
    Returns a list of dictionaries, each describing a vertical object.
    """
    grid = np.array(grid)
    objects = []
    visited = set()

    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                height = 0
                current_row = r
                while current_row < rows and grid[current_row, c] == color:
                    visited.add((current_row, c))
                    height += 1
                    current_row += 1
                
                objects.append({
                    'color': int(color),
                    'start_row': int(r),
                    'col': int(c),
                    'height': int(height)
                })
    return objects

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Convert to NumPy array for easier manipulation
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # Find vertical objects in the input grid
    vertical_objects = find_vertical_objects(input_grid)

    # Reconstruct objects horizontally
    for obj in vertical_objects:
        row_index = obj['start_row'] + obj['height'] -1
        
        if row_index < output_grid.shape[0]:
            for i in range(obj['height']):
                if obj['col'] - obj['height'] //2 + i < output_grid.shape[1] and  obj['col'] - obj['height'] //2 + i >=0 :
                     output_grid[row_index, obj['col'] - obj['height'] //2  + i ] = obj['color']
                elif obj['col'] + i < output_grid.shape[1]:
                      output_grid[row_index , obj['col'] + i] = obj['color']
    
    return output_grid.tolist()
```
