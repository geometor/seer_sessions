"""
Transforms the input grid by drawing diagonal lines (down and left) starting from each non-white pixel.
The lines extend until they hit the bottom or left edge of the grid.
The original non-white pixels are preserved in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Draws down-left diagonal lines from non-white pixels until grid edges.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            # Check if the cell contains a non-white color
            if color != 0:
                # Initialize the starting position for the diagonal line
                # One step down and one step left from the original pixel
                current_r = r + 1
                current_c = c - 1

                # While the current position is within the grid boundaries
                while 0 <= current_r < height and 0 <= current_c < width:
                    # Set the color of the cell in the output grid
                    output_grid[current_r, current_c] = color
                    # Update the current position: move down and left
                    current_r += 1
                    current_c -= 1

    return output_grid.tolist() # Return as list of lists, common ARC format