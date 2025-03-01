# ac0a08a4 • 010 • example_2 • investigate_coder

---
```python
"""
Expands each non-zero colored pixel in the input grid into a 3x3 block of the same color in the output grid, maintaining the relative positions. 
Leaves 0 (white) pixels as they are, resulting in a larger grid with expanded colored blocks.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for i in range(input_height):
        for j in range(input_width):
            # Conditional Expansion: If the cell value is not 0
            if input_grid[i, j] != 0:
                # Determine the color
                color = input_grid[i, j]
                # Calculate the top-left coordinates in the output grid for the 3x3 block
                start_row = i * 3
                start_col = j * 3
                # Fill the 3x3 block in the output grid
                for row_offset in range(3):
                    for col_offset in range(3):
                        output_grid[start_row + row_offset, start_col + col_offset] = color

    return output_grid
```
