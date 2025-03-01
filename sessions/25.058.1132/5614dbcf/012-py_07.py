"""
The transformation rule involves dividing the input grid into 3x3 subgrids and extracting a representative value from each subgrid to create a 3x3 output grid. The representative value is determined as follows:

1.  **Input Grid Division**: Divide the input grid into non-overlapping 3x3 subgrids. The input grid dimensions might not always be multiples of 3.
2.  **Representative Value Selection**:
    *   Within each subgrid, if the subgrid dimensions are multiples of 3x3 select the top-left pixel's value.
    *   If any dimension is not divisible by three the value will take the whole row and column into consideration.
3. **Output Grid Construction:** Arrange the extracted representative values into a 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine input dimensions
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Create output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through 3x3 subgrids
    for i in range(3):
        for j in range(3):
            # Calculate starting indices of the subgrid
            start_row = i * (input_height // 3)
            start_col = j * (input_width // 3)

            # Calculate the end indices of the subgrid
            end_row = min((i + 1) * (input_height // 3), input_height)
            end_col = min((j + 1) * (input_width // 3), input_width)
          
            # Extract the subgrid
            subgrid = input_grid[start_row:end_row, start_col:end_col]

            # If subgrid has a dimension of 0, skip.  This handles edge cases where the input grid is smaller than 3x3.
            if subgrid.size == 0:
                continue

            # Determine representative value.
            if input_height % 3 == 0 and input_width % 3 == 0:
                #take the top-left value of subgrid
                selected_value = input_grid[start_row][start_col]
            else:
                #take the first value from input grid
                selected_value = input_grid[start_row][start_col]

            # Place value in output grid
            output_grid[i][j] = selected_value

    return output_grid