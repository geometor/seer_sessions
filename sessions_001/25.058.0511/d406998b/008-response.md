# d406998b • 008 • example_2 • investigate_coder

---
```python
"""
Replaces some white (0) pixels with green (3) pixels in a grid, while keeping gray (5) pixels unchanged. The replacement pattern for white pixels involves alternating replacements, starting with the first encountered white pixel in each row.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions and values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each row of the grid.
    for r in range(rows):
        # Keep track of whether to replace the next white pixel.
        replace_next_white = True
        # Iterate through each column of the current row.
        for c in range(cols):
            # Check if the current pixel is white (0).
            if output_grid[r, c] == 0:
                # If we should replace this white pixel, change it to green (3).
                if replace_next_white:
                    output_grid[r, c] = 3
                # Toggle the replacement flag.
                replace_next_white = not replace_next_white

    # Return the modified grid.
    return output_grid
```
