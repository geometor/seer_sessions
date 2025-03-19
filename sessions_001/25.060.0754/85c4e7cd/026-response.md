# 85c4e7cd • 026 • refine_coder

---
```python
"""
The input grid is transformed into an output grid of the same dimensions by applying color swaps based on concentric rectangular layers. The layer of a pixel is determined by its minimum distance to any edge of the grid.  A special case exists for the center of grids with even dimensions, which is treated as a 2x2 square.
"""

import numpy as np

def get_layer(i, j, rows, cols):
    """
    Determines the layer of a pixel at (i, j) in a grid of size (rows, cols).
    """
    dist_top = i
    dist_bottom = rows - 1 - i
    dist_left = j
    dist_right = cols - 1 - j
    
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Check if the pixel is part of the 2x2 center (even dimensions)
    if rows % 2 == 0 and cols % 2 == 0:
        if i >= rows//2 -1 and i <= rows//2  and j >= cols//2 - 1 and j <= cols//2 :
            return rows//2 - 1

    return min_dist

def transform(input_grid):
    """
    Transforms the input grid according to the layer-based color mapping.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # Determine the layer of the current pixel
            layer = get_layer(i, j, rows, cols)

            # Apply color mapping based on the layer
            if layer == 0:
                if input_grid[i, j] == 7:  # Orange -> Green
                    output_grid[i, j] = 3
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 1:
                if input_grid[i, j] == 2:  # Red -> Blue
                    output_grid[i, j] = 1
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 2:
                if input_grid[i, j] == 4:  # Yellow -> Yellow (no change)
                    output_grid[i, j] = 4
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 3:
                if input_grid[i, j] == 1:  # Blue -> Red
                    output_grid[i, j] = 2
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer >= 4 :
                if rows % 2 == 0 and cols % 2 ==0: # Even dimension center (2x2)
                  if input_grid[i,j] == 3: #green -> orange
                      output_grid[i,j] = 7
                  else:
                      output_grid[i, j] = input_grid[i, j]
                else:  #Odd or non-center
                    if input_grid[i,j] == 3:
                        output_grid[i,j] = 7
                    else:
                        output_grid[i,j] = input_grid[i,j]
            else:
                output_grid[i,j] = input_grid[i,j]


    return output_grid
```
