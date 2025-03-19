# a3df8b1e • 008 • refine_coder

---
```python
"""
The transformation creates a checkerboard-like pattern within the grid.
The input grid is filled with a single color.
The output grid uses two colors:
- the color in the original input grid.
- the next color in the sequence (wrapping around from 9 back to 0).
    These two colors alternate in a checkerboard pattern.
    The top-left pixel of the output grid is the same as the input grid.
    Adjacent pixels, either horizontally or vertically, will be different
    colors.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input grid.
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the input color (all pixels in the input grid have the same color).
    input_color = input_grid[0, 0]
    # Determine the second color, which is the next color in the sequence.
    second_color = (input_color + 1) % 10

    # Iterate through each cell of the grid to create the checkerboard pattern.
    for r in range(rows):
        for c in range(cols):
            # If the sum of the row and column indices is even, use the input color.
            if (r + c) % 2 == 0:
                output_grid[r, c] = input_color
            # Otherwise, use the second color.
            else:
                output_grid[r, c] = second_color

    return output_grid
```
