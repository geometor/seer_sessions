"""
1.  **Input:** A grid of variable size containing pixel values (0-9).
2.  **Output:** A 4x4 grid.
3.  **Blue Row Identification:** Find the row index in the input grid where all pixels are blue (value 1).
4.  **Row 1 Construction:** Copy the last four elements of the first row of the input grid to the first row of the output grid.
5.  **Row 2 Construction:** Copy the last four elements of the second row of the input grid to the second row of the output grid.
6.  **Row 3 Construction:** Fill the third row of the output grid with orange (value 7).
7.  **Row 4 Construction:** Copy the last four elements of the row immediately below the blue row in the input grid to the fourth row of the output grid.
8.  **Output Dimensions:** The output is always a 4x4 grid.
"""

import numpy as np

def find_blue_row(grid):
    """Finds the index of the row where all pixels are blue (1)."""
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