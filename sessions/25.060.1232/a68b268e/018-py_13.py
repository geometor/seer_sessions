"""
1.  **Input Grid:** The input is a grid of variable size.

2.  **Blue Row:** Identify the horizontal row where all pixels are blue (value 1).

3.  **Output Grid:** The output is a 4x4 grid.

4.  **First Row Construction:**
    *   Take the values of row 1 of the input grid and, starting from the right, copy 4 values to row 1 of the output grid.

5.  **Second Row Construction:**
    *   Take the values of row 2 of the input grid, and, starting from the right, copy 4 values to row 2 of the output grid.

6.  **Third Row Construction:**
    *   The third row of the output grid is always filled with orange (value 7).

7.  **Fourth Row Construction:**
    *    Take the values of the row below the blue row of the input grid, and, starting from the right, copy 4 values to row 4 of the output grid.

8. **Dimensions:** The output grid is always 4x4
"""

import numpy as np

def find_blue_row(grid):
    for i in range(grid.shape[0]):
        if all(grid[i, :] == 1):
            return i
    return None  # No blue row found
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)
    
    #find blue row
    blue_row_index = find_blue_row(input_grid)

    # construct first row
    input_row_1 = input_grid[0]
    for j in range(output_grid.shape[1]):
        output_grid[0,j] = input_row_1[j + input_grid.shape[1]-output_grid.shape[1]]
        
    # construct second row
    input_row_2 = input_grid[1]
    for j in range(output_grid.shape[1]):
        output_grid[1,j] = input_row_2[j + input_grid.shape[1]-output_grid.shape[1]]

    # construct third row (all orange)
    output_grid[2,:] = 7

    # construct fourth row
    input_row_blue_plus_one = input_grid[blue_row_index + 1]
    for j in range(output_grid.shape[1]):
        output_grid[3,j] = input_row_blue_plus_one[j + input_grid.shape[1]-output_grid.shape[1]]
    

    return output_grid