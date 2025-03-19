# 0a938d79 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule depends on the arrangement of non-zero pixels in the input grid.

If non-zero pixels are in the same row:
    The output grid's height matches the input grid's height, while the width can either grow
    or match. Each non-zero pixel's color extends vertically down its column, creating
    alternating colored columns based on the initial positions.

If non-zero pixels are on different rows:
    The output replicates colored rows based on color location, repeating this
    to create the output grid height. The width of the rows are extended to match
    the input grid.
"""

import numpy as np

def get_nonzero_pixels(grid):
    # Find coordinates and colors of non-zero pixels
    rows, cols = np.where(grid != 0)
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def transform(input_grid):
    input_grid = np.array(input_grid)
    nonzero_pixels = get_nonzero_pixels(input_grid)

    if not nonzero_pixels:
        return input_grid.tolist()  # Return original if no non-zero pixels

    # Check if all non-zero pixels are in the same row
    first_row = nonzero_pixels[0][0]
    same_row = all(pixel[0] == first_row for pixel in nonzero_pixels)
    
    if same_row:
        # initialize output
        output_grid = np.zeros_like(input_grid)
        
        # Extend colors vertically
        for r, c, color in nonzero_pixels:
            output_grid[:, c] = color
    else:
        # different rows
        rows = [p[0] for p in nonzero_pixels]
        colors = [p[2] for p in nonzero_pixels]
        
        # new height with repeating pattern
        h, w = input_grid.shape
        output_height = h * len(colors) if h * len(colors) < 30 else 30
        
        output_grid = np.zeros((output_height, w),dtype=int)        

        for i in range(output_height):
          color_index = i % len(colors)
          output_grid[i,:] = colors[color_index]
        

    return output_grid.tolist()
```
