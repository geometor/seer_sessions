"""
1.  **Initialization:** Create an output grid identical to the input grid in dimensions, but will be adjusted below.

2.  **Color 2 Preservation:** Iterate through each pixel of the input grid. If a pixel has a value of 2 (red), copy that value to the corresponding pixel in the output grid.

3.  **Color 5 Removal/Ignore:** Pixels with value 5 will not directly exist in the output.

4.  **Color 0 Transformation:** Iterate through each pixel of the *input* grid.
    *   If a pixel in the input grid has the value of 0, and that location in the *output* grid does not have a value of 2, check its adjacent pixels (up, down, left, right, and diagonals) in the *input* grid.
    *    If *any* of the adjacent pixels in the *input* grid have a value of 2 (red), change the value of that pixel to 1 (blue) in the *output* grid.
    *   If a pixel has value 0 and is not adjacent to any pixels with value 2, the pixel remains unchanged.
5. **Return:** Once every input pixel is evaluated, the output grid, which will be a combination of 0, 1, and 2 values, will represent the solution.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the neighbors of a cell including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:  # Skip the cell itself
                continue
            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append(grid[neighbor_row, neighbor_col])
    return neighbors

def transform(input_grid):
    # initialize output_grid with the same dimensions as input_grid
    output_grid = np.zeros_like(input_grid)
     
    # Iterate through each pixel of the input and perform actions
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            # Color 2 Preservation:
            if input_grid[row, col] == 2:
                output_grid[row, col] = 2
            # Color 0 Transformation:
            elif input_grid[row,col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                if 2 in neighbors:
                    output_grid[row,col] = 1
                # else:
                # if the 0s remain 0, no operation necessary due to np.zeros initialization
    return output_grid