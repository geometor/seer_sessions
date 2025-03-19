# 85c4e7cd • 025 • refine_coder

---
```python
"""
The transformation involves processing a grid in concentric layers, starting from the outermost edge (layer 0) and moving inwards.  Each layer has a specific set of rules for mapping input colors to output colors. The rules are as follows:

1.  **Layer 0:**
    *   If the input color is orange (7), change it to green (3).
    *   Otherwise, keep the original color
2.  **Layer 1:**
    *   If the input color is red (2), change it to blue (1).
    *   Otherwise, keep the original color
3.  **Layer 2:**
      * If the input color is yellow (4), change it to yellow (4).
      * Otherwise, keep the original color.
4.  **Layer 3:**
    *   If the input color is blue (1), change it to red (2).
    *   Otherwise, keep the original color.
5.  **Layer 4:**
    *  If the input color is green (3), change it to orange (7).
    *   Otherwise, keep the original color.
6.  **Other Layers:** (Currently not observed, maintain a default of keeping original colors)

The layer of a pixel is determined by its minimum distance to any edge of the grid. If grid dimensions are even, the central four pixels form a single layer at `grid.shape[0]//2 -1`. If grid dimensions are odd, the central single pixel is a later at `min(dist_top, dist_bottom, dist_left, dist_right)`.
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

    # Check if the pixel is part of the 2x2 center
    if rows % 2 == 0 and cols % 2 == 0: #even
        if i >= rows//2 -1 and i <= rows//2  and j >= cols//2 - 1 and j <= cols//2 :
            return rows//2 - 1
    else: #odd
        if i == rows//2 and j == cols//2:
          return min_dist

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
                if input_grid[i, j] == 7:
                    output_grid[i, j] = 3
                else:
                    output_grid[i,j] = input_grid[i,j] #handles the outside if different
            elif layer == 1:
                if input_grid[i, j] == 2:
                    output_grid[i, j] = 1
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 2:
                if input_grid[i, j] == 4:
                    output_grid[i, j] = 4
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 3:
                if input_grid[i, j] == 1:
                    output_grid[i, j] = 2
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 4:
                if input_grid[i, j] == 3:
                        output_grid[i, j] = 7
                else:
                    output_grid[i,j] = input_grid[i,j]
            else:
                output_grid[i, j] = input_grid[i,j] #default

    return output_grid
```
