"""
Iterates through each cell of the input grid. If a cell contains the value 4,
it checks its North (above) and West (left) neighbors. If both neighbors are 0
(treating cells outside the grid boundaries as 0), the cell's value is changed
to 0 in the output grid. Otherwise, the cell's value remains unchanged (either 0 or 4).
"""

import numpy as np

def get_neighbor_value(grid, r, c):
    """
    Safely gets the value of a cell at (r, c) in the grid.
    Returns 0 if the coordinates are out of bounds.
    """
    rows, cols = grid.shape
    if 0 <= r < rows and 0 <= c < cols:
        return grid[r, c]
    else:
        # Treat cells outside the grid boundaries as 0
        return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array if it's not already
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape

    # Initialize output_grid as a copy of the input_grid
    # This handles keeping 0s as 0s and initially keeps 4s as 4s
    output_grid = np.copy(input_grid_np)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains the value 4
            if input_grid_np[r, c] == 4:
                # Get the value of the North neighbor (r-1, c)
                north_neighbor = get_neighbor_value(input_grid_np, r - 1, c)

                # Get the value of the West neighbor (r, c-1)
                west_neighbor = get_neighbor_value(input_grid_np, r, c - 1)

                # Check the condition: North neighbor is 0 AND West neighbor is 0
                if north_neighbor == 0 and west_neighbor == 0:
                    # Change the corresponding cell in the output grid to 0
                    output_grid[r, c] = 0
                # Otherwise (else condition), the cell in output_grid already
                # retains its original value (4) from the copy operation,
                # satisfying step 2d and 3.

    return output_grid.tolist() # Return as list of lists if preferred, or just output_grid for numpy array