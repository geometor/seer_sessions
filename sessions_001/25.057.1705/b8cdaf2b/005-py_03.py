"""
1.  **Examine the last row of the input grid.**
2.  **Find the center element** of the input's last row (index 4).
3.  **Copy the center element of the last row** from the input to all values in the *first* row of the output grid.
4. **If all values in the input grid are the same**, then the last row of the output grid is the same as the last row of the input grid, *except* for the last element, which is the center element found in step 2.
5. **All other rows remain the same** between the input and output grids.
"""

import numpy as np

def get_center_element(row):
    """Returns the center element of a given row."""
    return row[len(row) // 2]

def are_all_elements_same(grid):
    """Checks if all elements in the grid are the same."""
    first_element = grid.flatten()[0]
    return np.all(grid == first_element)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid = np.array(input_grid)
    last_row = input_grid[-1]

    # change output pixels
    center_element = get_center_element(last_row)

    #Replace the first row
    output_grid[0, :] = center_element
    
    if are_all_elements_same(input_grid):
      output_grid[-1, :] = input_grid[-1,:]
      output_grid[-1,-1] = center_element

    return output_grid.tolist()