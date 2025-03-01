# ce22a75a • 002 • example_2 • investigate_coder

---
```python
"""
1. **Initialization:** Start with the given input grid.
2. **Locate Gray Pixels:** Iterate through each cell of the input grid. Identify the coordinates (row, column) of all pixels with a value of 5 (gray).
3. **Replace with Blue Blocks:** For each gray pixel found:
    a. Calculate the top-left corner coordinates of a 3x3 block, centered on the gray pixel. This is done by subtracting 1 from both the row and column of the gray pixel.
    b. If the top-left, bottom-right, or intermediate cells of the block are out of bounds, use `0` value, otherwise use a value of 1.
    c. Replace the gray pixel and its surrounding 8 neighbors in a 3x3 area with blue pixels (value 1) at the calculated position.
4. **Output:** The resulting grid, after all gray pixels have been replaced, is the output grid. Keep `0` values unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing gray pixels (5) with 3x3 blue blocks (1).
    """
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # output_grid = np.zeros((rows, cols), dtype=int) # don't zero out

    # Iterate through the input grid to find gray pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] == 5:
                # Calculate top-left corner of the 3x3 block
                top_left_row = i - 1
                top_left_col = j - 1

                # Replace with a 3x3 blue block
                for x in range(3):
                    for y in range(3):
                        curr_row = top_left_row + x
                        curr_col = top_left_col + y
                        
                        # check bounds
                        if 0 <= curr_row < rows and 0 <= curr_col < cols:
                           output_grid[curr_row][curr_col] = 1
                        # out of bounds pixels are value 0 by default

    return output_grid
```
