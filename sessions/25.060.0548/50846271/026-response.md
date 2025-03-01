# 50846271 • 026 • example_4 • investigate_coder

---
```python
"""
Identify a red (2) cross-shaped object in the input grid. Change the central red pixel to azure (8).
"""

import numpy as np

def find_cross_center(grid):
    # Find all red pixels
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    # Calculate the centroid of the red pixels
    center = red_pixels.mean(axis=0)
    
    # Find the closest actual red pixel to the centroid
    distances = np.sqrt(np.sum((red_pixels - center)**2, axis=1))
    closest_pixel_index = np.argmin(distances)
    center_pixel = tuple(red_pixels[closest_pixel_index])
    return center_pixel

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the center of the cross
    center = find_cross_center(output_grid)

    if center is not None:
         # Change the center pixel to azure (8)
         output_grid[center] = 8


    return output_grid
```
