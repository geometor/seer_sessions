# 22233c11 • 016 • example_3 • investigate_coder

---
```python
"""
1. Copy Green Pixels: Copy all pixels with the value '3' (green) from the input grid to the same positions in the output grid.
2. Place Azure Pixels Diagonally: For each green pixel in the input grid, if an azure pixel can be placed at the following offsets, place an azure pixel in the output grid:
    *   +1 row, -2 column and -1 row, +2 columns.
    *  In other words, place an Azure pixel at one row and two cols, towards top-right and bottom-left corners, relative to the current green pixel, considering the origin as top-left.
3. Fill empty cells with zeros: Fill the other cells of the output with 0.

"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Copy green pixels (value 3)
            if input_grid[i, j] == 3:
                # The green pixel is already in the output_grid due to the initialization with np.copy()

                # Calculate positions for azure pixels
                azure_positions = [(i - 1, j + 2), (i + 1, j - 2)]

                # Place azure pixels (value 8) at calculated positions if within bounds
                for row, col in azure_positions:
                    if 0 <= row < rows and 0 <= col < cols:
                        output_grid[row, col] = 8

    return output_grid
```
