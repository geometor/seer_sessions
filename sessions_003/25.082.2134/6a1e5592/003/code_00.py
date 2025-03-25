"""
1.  **Initialization:** Create an output grid.
2.  **Preserve '2's:** Copy all pixels with value '2' (red) from the input grid to the output grid.
3.  **Remove '5's:** Pixels with the value '5' (gray) in the input grid are not copied to the output grid and have no bearing on the transformation.
4.  **Conditional '0' Transformation:** For each pixel with value '0' (white) in the *input* grid:
    *   Check its immediate neighbors (up, down, left, right, and diagonals) in the *input* grid.
    *   If *any* of these neighbors have a value of '2' (red), change the corresponding pixel in the *output* grid to '1' (blue). The key here is that a 0 in the input becomes a 1 in the output *only* if it is directly adjacent to a 2 in the input.
5. **Remove empty rows**: if there is any all 0 row in output, remove it from the
   output

6.  **Return:** The output grid now contains the transformed image.
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
     
    # Iterate through each pixel of the input
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
            # Color 5 is implicitly removed because output is initialized to 0s.
            # else:  # input is 5 -- do nothing

    # Remove empty rows
    non_empty_rows = []
    for row in range(output_grid.shape[0]):
        if np.any(output_grid[row] != 0): # Check if the row has any non-zero elements
            non_empty_rows.append(output_grid[row])

    if len(non_empty_rows) > 0:
      output_grid = np.array(non_empty_rows)
    else:
      output_grid = np.array([]) # return empty grid

    return output_grid