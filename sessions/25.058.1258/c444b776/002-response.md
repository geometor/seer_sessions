# c444b776 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation duplicates the non-yellow pixels from the top section of the grid (above the yellow line) to the bottom section (below the yellow line), maintaining their respective column positions, while keeping the yellow line in place.
"""

import numpy as np

def find_yellow_line(grid):
    # Iterate through rows to find a row where all non-zero pixels are yellow (4)
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row if pixel != 0):
            return i
    return -1  # Return -1 if no yellow line is found

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    yellow_line_row = find_yellow_line(input_grid)

    if yellow_line_row == -1:
        return output_grid # No transformation if no yellow line

    # Iterate through the input grid above the yellow line
    for r in range(yellow_line_row):
        for c in range(input_grid.shape[1]):
             # Copy non-yellow pixels to corresponding position below the line
            if input_grid[r, c] != 4 and input_grid[r,c] != 0:
                output_grid[r + yellow_line_row + 1,c ] = input_grid[r, c]

    return output_grid
```
