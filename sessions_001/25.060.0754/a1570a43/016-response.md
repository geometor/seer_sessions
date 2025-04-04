# a1570a43 • 016 • example_3 • investigate_coder

---
```python
"""
Transforms the input grid by rotating a cross shape formed by red (2) pixels 90 degrees clockwise and maintaining the positions of green (3) pixels. The bounding box of the red cross is shifted one pixel down.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    return coords

def rotate_cross(coords):
    # Rotate the coordinates of red cross 90 degrees clockwise around its center.
    if len(coords) == 0:
      return []
    
    center = np.mean(coords, axis=0)
    rotated_coords = []
    for coord in coords:
        # Translate to origin
        x = coord[1] - center[1]
        y = coord[0] - center[0]
        # Rotate 90 degrees clockwise
        new_x = -y
        new_y = x
        # Translate back to original position
        rotated_coords.append([int(new_y + center[0]+1), int(new_x + center[1])])
    return np.array(rotated_coords)


def transform(input_grid):
    # Initialize output grid with the same dimensions and filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Find green and red pixels.
    green_pixels = find_object(input_grid, 3)
    red_pixels = find_object(input_grid, 2)
    
    #rotate and shift red pixels
    rotated_red_pixels = rotate_cross(red_pixels)

    # Place green pixels in the output grid.
    for r, c in green_pixels:
        output_grid[r, c] = 3

    # Place rotated red pixels in the output grid, handling out-of-bounds errors.
    for r, c in rotated_red_pixels:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          output_grid[r,c] = 2

    return output_grid
```
