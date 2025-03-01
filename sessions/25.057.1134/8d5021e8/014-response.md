# 8d5021e8 • 014 • example_3 • investigate_coder

---
```python
"""
Expands a 3x2 input grid to a 9x4 output grid. Gray (5) pixels in the input
expand to 2x2 blocks in the output, or smaller when adjacent, and white (0)
pixels fill the remaining space.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = 9, 4
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 5:
                # Calculate the starting position for the expanded block
                start_row = i * 3
                start_col = j * 2

                # Check for adjacent gray pixels to adjust block size and
                # avoid overlaps.
                # we will use a simple approach and expand 2x2 and reduce it
                # later if necessary

                # default is 2x2 cell, may be reduced
                row_end = min(start_row + 2, output_rows) # limit
                col_end = min(start_col + 2, output_cols)

                # corners
                top_left = i > 0 and j > 0 and input_grid[i-1,j-1] == 5
                top_right = i > 0 and j < input_cols - 1 and input_grid[i-1,j+1] == 5
                bottom_left = i < input_rows - 1 and j > 0 and input_grid[i+1,j-1] == 5
                bottom_right = i < input_rows - 1 and j < input_cols-1 and input_grid[i+1,j+1] == 5

                if top_left:
                    output_grid[start_row,start_col] = 5
                if top_right:
                    output_grid[start_row,start_col+1] = 5
                if bottom_left:
                    output_grid[start_row+1,start_col] = 5
                if bottom_right:
                    output_grid[start_row + 1, start_col + 1] = 5
                
                # sides, do after corners so they will reduce corner if necessary
                top = i > 0 and input_grid[i-1,j] == 5
                left = j > 0 and input_grid[i, j-1] == 5
                bottom = i < input_rows - 1 and input_grid[i+1,j] == 5
                right = j < input_cols - 1 and input_grid[i, j+1] == 5

                if top:
                    col_end = min(start_col + 2, output_cols)
                    row_end = min(start_row + 1, output_rows)
                if bottom:
                    col_end = min(start_col + 2, output_cols)
                    row_end = min(start_row + 1, output_rows)      
                if left:
                    col_end = min(start_col + 1, output_cols)
                    row_end = min(start_row + 2, output_rows)
                if right:
                    col_end = min(start_col + 1, output_cols)
                    row_end = min(start_row + 2, output_rows)


                # Fill the block, which will be 2x2, or less due to neighbors
                for row in range(start_row,row_end):
                    for col in range(start_col, col_end):
                         output_grid[row,col] = 5

    return output_grid
```
