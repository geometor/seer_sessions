```python
"""
Transforms an input grid by moving the right-most gray (5) pixel in each row to the first column,
and shifts right-most non-zero, non-gray pixel to column 0. Other non-zero,
non-gray pixels maintain their row and their column, unless a non-zero, non-gray
pixel is to the left of them. Fills remaining cells with 0.
"""

import numpy as np

def get_rightmost_value(row, value):
    """
    Finds the rightmost occurence of a value in a 1D array
    """
    indices = np.where(row == value)[0]
    if indices.size > 0:
        return indices[-1]
    return -1
    

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # iterate over rows
    for i in range(rows):
        # Find rightmost gray pixel (5)
        gray_index = get_rightmost_value(input_grid[i], 5)
        
        # Find rightmost non-zero and non-gray pixel.
        non_zero_non_gray_indices = np.where((input_grid[i] != 0) & (input_grid[i] != 5))[0]
        non_zero_non_gray_index = -1
        if non_zero_non_gray_indices.size > 0:
           non_zero_non_gray_index = non_zero_non_gray_indices[-1]

        # Move rightmost gray and the other color.
        if gray_index != -1:
            output_grid[i, 0] = 5

        if non_zero_non_gray_index != -1:
             output_grid[i, 1] = input_grid[i, non_zero_non_gray_index]
        
        # Move other colors
        current_col = 2
        for j in range(cols):
             if input_grid[i,j] != 0 and input_grid[i,j] != 5 and j != non_zero_non_gray_index:
                output_grid[i,current_col] = input_grid[i,j]
                current_col += 1

    return output_grid.tolist()
```