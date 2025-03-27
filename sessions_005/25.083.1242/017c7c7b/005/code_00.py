"""
1.  **Color Transformation:** Iterate through each cell of the input grid. If a cell is blue (1), change it to red (2) in the output grid. Otherwise, keep the original color.
2.  **Row Appending:**
    *   Count the total number of blue pixels in the *original* input grid.
    *   Calculate the number of rows to append: Divide the total number of blue pixels by the number of columns in the input grid, using integer division (floor division).
    *  Create a copy of what *would have been* the last row of the output grid *after* performing only the color transformation in step 1.
    *   Append the copied row to the output grid the calculated number of times.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1]), dtype=int)

    # change output pixels 
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 1:
                output_grid[r, c] = 2
            else:
                output_grid[r,c] = input_grid[r,c]
    
    #count blue pixels
    n_blue = np.sum(input_grid == 1)

    #calculate number of rows to append
    n_appended = n_blue // input_grid.shape[1]

    # Create a copy of the last row after color transformation
    last_row_transformed = output_grid[input_grid.shape[0]-1, :].copy()

    #resize output grid
    new_shape = (output_grid.shape[0] + n_appended, output_grid.shape[1])
    output_grid.resize(new_shape, refcheck=False)


    #copy last row to a new one and append
    for i in range(n_appended):
        output_grid[input_grid.shape[0] + i, :] = last_row_transformed


    return output_grid.tolist()