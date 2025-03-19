# 007bbfb7 • 002 • example_5 • investigate_coder

---
```python
"""
The transformation expands a 3x3 input grid into a 9x9 output grid. Each cell in the input grid, based on its color and position, dictates a 3x3 pattern in the corresponding section of the output grid. Background color (0) in the input generally results in the corresponding output section remaining background. Other colors have specific infill patterns within their 3x3 blocks.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid to a 9x9 output grid based on color-specific rules.
    """
    output_grid = np.zeros((9, 9), dtype=int)  # Initialize output grid with background color (0)

    for i in range(3):  # Iterate through rows of input grid
        for j in range(3):  # Iterate through columns of input grid
            color = input_grid[i, j]
            output_block_start_row = i * 3
            output_block_start_col = j * 3

            # Apply color-specific rules
            if color == 7:  # Orange
                for row in range(3):
                    for col in range(3):
                        if input_grid[i,j] == 7:
                            output_grid[output_block_start_row + row, output_block_start_col + col] = 7
            elif color == 4:  # Yellow
                output_grid[output_block_start_row, output_block_start_col] = 4 #top-left
                output_grid[output_block_start_row, output_block_start_col + 2] = 4 #top-right
                output_grid[output_block_start_row + 2, output_block_start_col] = 4 #bottom-left
                output_grid[output_block_start_row + 2, output_block_start_col + 2] = 4 #bottom-right

            elif color == 2:  # Red
                output_grid[output_block_start_row, output_block_start_col] = 2
                output_grid[output_block_start_row + 2, output_block_start_col] = 2
                output_grid[output_block_start_row + 2, output_block_start_col + 2] = 2
            elif color == 6:  # Magenta
                output_grid[output_block_start_row, output_block_start_col] = 6
                output_grid[output_block_start_row, output_block_start_col + 1] = 6
                output_grid[output_block_start_row + 1, output_block_start_col] = 6
                output_grid[output_block_start_row + 2 , output_block_start_col + 1] = 6
                output_grid[output_block_start_row + 2, output_block_start_col + 2] = 6


            # color == 0 is already handled since we initialized to 0

    return output_grid
```
