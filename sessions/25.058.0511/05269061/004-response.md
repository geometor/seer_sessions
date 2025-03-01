# 05269061 • 004 • refine_coder

---
```python
"""
The transformation rule identifies the colors in the input grid and uses them to construct the output grid. It operates on vertical slices of 3 rows. For each 3xn slice (where n is the width of the input), it places those same colors into the output grid. Subsequent slices shift the colors downward by one position, wrapping the bottom color to the top. Finally, if a cell in the output grid has the same color as the cell directly above it, that cell is changed to black (0).
"""

import numpy as np

def shift_colors(colors):
    """Shifts the colors down by one position, wrapping the last color to the top."""
    return [colors[-1]] + colors[:-1]

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Process the grid in 3-row slices
    for i in range(0, rows, 3):
        # Extract the colors for the current slice
        slice_colors = []

        #get unique colors in the slice
        for row in range(i,min(i+3,rows)):
           for col in range(cols):
               color=input_grid[row,col]
               if color not in slice_colors:
                   slice_colors.append(color)


        #fill output slice
        for j in range(min(3,rows-i)):  # Handle cases where fewer than 3 rows remain
            for k in range(cols):
                output_grid[i + j, k] = slice_colors[j%len(slice_colors)] if len(slice_colors) > 0 else 0
        # Shift colors for the next slice
        if len(slice_colors)> 0:
            slice_colors = shift_colors(slice_colors)


    # Apply the black color rule
    for i in range(1, rows):
        for j in range(cols):
            if output_grid[i, j] == output_grid[i - 1, j]:
                output_grid[i, j] = 0

    return output_grid
```
