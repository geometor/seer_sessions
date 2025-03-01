# 85c4e7cd • 022 • example_4 • investigate_coder

---
```python
"""
The input grid is transformed into an output grid of the same dimensions. 
The transformation involves swapping colors based on concentric rectangular layers.

1. **Identify Layers:** The grid is conceptually divided into concentric layers:
   - Layer 1: Outermost border (orange -> green)
   - Layer 2: 1-pixel thick rectangle inside Layer 1 (red -> blue)
   - Layer 3: 1-pixel thick rectangle inside Layer 2 (yellow -> yellow)
   - Layer 4: 1-pixel thick rectangle inside Layer 3 (blue -> red)
   - Layer 5: Innermost 2x2 square (green -> orange)

2. **Color Mapping:**  A color mapping is applied based on these layers.

3. **Apply Mapping:**  Each pixel's color in the input grid is transformed based on its layer's mapping.
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
                if rows % 2 == 0: #only applies to even
                    if input_grid[i,j] == 3:
                        output_grid[i, j] = 7
                    else:
                        output_grid[i,j] = input_grid[i,j]
                else:
                    if input_grid[i, j] == 3:
                        output_grid[i,j] = 7
                    else:
                        output_grid[i,j] = input_grid[i,j]
            else:
                output_grid[i, j] = input_grid[i,j] #default

    return output_grid
```
