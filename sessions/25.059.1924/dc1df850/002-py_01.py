"""
Iterate through each pixel in the input grid. Identify non-zero pixels. Preserve the original non-zero colored pixels in the output grid. For each non-zero pixel, examine its four immediate neighbors (up, down, left, and right). If a neighbor is within the grid boundaries and has a value of 0 in the input grid, change its value to 1 (blue) in the output grid. Pixels not neighboring a non-zero cell remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the halo rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Identify non-zero pixels
            if input_grid[row, col] != 0:
                # Preserve original non-zero pixel
                output_grid[row, col] = input_grid[row, col]

                # Examine neighbors
                neighbors = [
                    (row - 1, col),  # Up
                    (row + 1, col),  # Down
                    (row, col - 1),  # Left
                    (row, col + 1),  # Right
                ]

                for n_row, n_col in neighbors:
                    # Check boundaries and if neighbor was zero in input
                    if 0 <= n_row < rows and 0 <= n_col < cols and input_grid[n_row, n_col] == 0:
                        # Change to blue (1)
                        output_grid[n_row, n_col] = 1
    
    return output_grid.tolist()