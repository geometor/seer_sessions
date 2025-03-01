# 4c5c2cf0 • 024 • refine_coder

---
```python
"""
The transformation rule involves identifying a blue (1) cluster in the input grid,
mirroring it horizontally, and adjoining the copy to the right of the original,
while keeping the azure (8) and white (0) pixels unchanged. Crucially,
connectivity (including diagonal) within the blue cluster must be preserved
in the mirrored copy.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Calculate the bounding box.
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()

    object_block = grid[min_row:max_row+1, min_col:max_col+1]
    
    return object_block, min_row, min_col, max_col

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the blue (1) object.
    blue_object, min_row, min_col, max_col = find_object(input_grid, 1)

    if blue_object is not None:
        # Determine the size of the blue object block.
        h, w = blue_object.shape
        
        # Iterate through the blue object's bounding box.
        for r in range(h):
            for c in range(w):
                # Only mirror blue pixels.
                if blue_object[r, c] == 1:
                    # Mirror horizontally:  new_col = max_col + (max_col - (min_col + c) ) + 1
                    new_c = 2 * max_col - (min_col + c) + 1
                    output_grid[min_row + r, new_c] = 1

                    # Check for neighbors (including diagonals) and connect them.
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip the pixel itself.
                            
                            # Check bounds within the original object
                            if 0 <= r + dr < h and 0 <= c + dc < w:
                                if blue_object[r + dr, c + dc] == 1:
                                    # Calculate neighbor's mirrored position.
                                    neighbor_new_c = 2 * max_col - (min_col + c + dc) +1
                                    output_grid[min_row + r + dr, neighbor_new_c] = 1
    return output_grid
```
