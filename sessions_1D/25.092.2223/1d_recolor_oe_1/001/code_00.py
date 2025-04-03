import numpy as np

"""
Recolor red pixels based on vertical adjacency.

1. Create an output grid with the same dimensions as the input grid.
2. Iterate through each cell (pixel) of the input grid.
3. If the input cell is white (0), the output cell remains white (0).
4. If the input cell is red (2):
    a. Check if there is a cell directly below it within the grid boundaries.
    b. If there is a cell below and it is also red (2), the output cell becomes maroon (9).
    c. Otherwise (no cell below or the cell below is not red), the output cell becomes orange (7).
5. Return the modified grid.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the recoloring rules based on vertical adjacency.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize output_grid as a copy of the input grid.
    # This handles the white(0) pixels correctly by default.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (2)
            if input_grid[r, c] == 2:
                # Check if there is a row below the current row
                is_red_below = False
                if r + 1 < height:
                    # Check if the pixel directly below is also red (2)
                    if input_grid[r + 1, c] == 2:
                        is_red_below = True
                
                # Apply the transformation rule
                if is_red_below:
                    output_grid[r, c] = 9 # Change to maroon
                else:
                    output_grid[r, c] = 7 # Change to orange
            # No action needed for white (0) pixels as we started with a copy

    return output_grid
