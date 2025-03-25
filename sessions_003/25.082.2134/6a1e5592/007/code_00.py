"""
1.  **Copy Reds:** Create an output grid of the same dimensions as the input, initially filled with zeros (white). Copy all red pixels (value '2') from the input grid to the corresponding positions in the output grid.

2.  **Propagate Blue Conditionally:** For *each* white pixel (value '0') in the *input* grid:
    *   Check its immediate neighbors (up, down, left, right, and diagonals) in the *input* grid.
    *   If *any* neighbor is red (value '2'), set the corresponding pixel in the *output* grid to blue (value '1').

3.  **Remove Empty Bottom Rows:** Examine the rows of the *output* grid, starting from the bottom. Remove any rows that contain *only* zeros (white). Stop removing rows when a row with a non-zero value is found.

4.  **Output:** Return the resulting `output_grid`.
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
    # Initialize output_grid with the same dimensions as input_grid, filled with 0s
    output_grid = np.zeros_like(input_grid)
     
    # Iterate through each pixel of the input
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            # Copy Reds
            if input_grid[row, col] == 2:
                output_grid[row, col] = 2

    # Propagate Blue
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                if 2 in neighbors:
                    output_grid[row,col] = 1


    # Remove empty rows from the bottom
    non_empty_rows = []
    for row in range(output_grid.shape[0]):
        if np.any(output_grid[row] != 0): # Check if the row has any non-zero elements
            non_empty_rows.append(output_grid[row])
    
    if len(non_empty_rows) > 0:
        output_grid = np.array(non_empty_rows)
    else:
        output_grid = np.array([]) # return empty grid

    return output_grid