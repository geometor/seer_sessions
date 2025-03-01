# 137eaa0f • 010 • example_2 • investigate_coder

---
```python
"""
Extracts non-zero pixels from the input grid and arranges them in a 3x3 output grid, preserving their relative positions and colors, as well as horizontal adjacency.
"""

import numpy as np

def get_nonzero_pixels(grid):
    # Find coordinates and values of non-zero pixels
    rows, cols = np.nonzero(grid)
    return [(rows[i], cols[i], grid[rows[i], cols[i]]) for i in range(len(rows))]

def transform(input_grid):
    # Find all non-zero pixels and their original positions.
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # Sort the pixels based on their appearance row-major.
    sorted_pixels = sorted(nonzero_pixels, key=lambda x: (x[0], x[1]))

    # Create an empty 3x3 output grid.
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the output grid with the sorted non-zero pixel values.
    pixel_index = 0
    for row in range(3):
        for col in range(3):
            if pixel_index < len(sorted_pixels):
                output_grid[row, col] = sorted_pixels[pixel_index][2]
                pixel_index += 1
    
    return output_grid
```
