"""
1.  **Initialization:** Create an output grid initialized with all zeros, having the same dimensions as the input grid.

2.  **Copy Reds:** Iterate through each pixel in the input grid. If a pixel's value is '2' (red), copy it directly to the corresponding position in the output grid.

3.  **Iterative Blue Propagation, Remove 5s**:
     - If a pixel in *input* is 0:
        - Check if *any* of its immediate neighbors (up, down, left, right, and diagonals) in the *input* grid are '2' (red).
        - If a red neighbor is found, set the corresponding pixel in the *output* grid to '1' (blue).
        - Repeat this check for *all* zeros in the input, including propagating to subsequent rows if they also have neighboring 2's.
     - Pixels with the value '5' (gray) in the input grid are ignored, they have no effect, resulting in 0s in corresponding cells of output.

4.  **Remove Empty Rows:** After processing all pixels, iterate through the rows of the *output* grid. If a row contains *only* zeros, remove it from the output grid.

5.  **Return:** The modified output grid represents the transformed image.
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
            # Color 2 Preservation:
            if input_grid[row, col] == 2:
                output_grid[row, col] = 2

    # Iterate again, propagating '1's downwards.  This needs a separate loop
    # so the reds are copied first.
    for row in range(rows):
        for col in range(cols):
            # Color 0 Transformation:
            if input_grid[row,col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                if 2 in neighbors:
                    output_grid[row,col] = 1
            elif output_grid[row, col] == 1: # propagate down
                neighbors = get_neighbors(output_grid, row, col)
                if 1 in neighbors:
                    output_grid[row,col] = 1


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