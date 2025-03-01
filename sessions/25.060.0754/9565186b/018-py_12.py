"""
1.  **Identify Azure Pixels:** Iterate through each pixel of the input grid, focusing on pixels that are azure (color code 8).

2.  **Neighbor Analysis:** For each azure pixel, examine its eight immediate neighbors (up, down, left, right, and diagonals).

3.  **Conditional Color Change:**
    *   If *all* eight neighbors are also azure, change the pixel's color to gray (color code 5).
    *   If *exactly seven* neighbors are azure and *one* neighbor is *not* azure (any other color, including background color 0), the pixel *remains* azure (color code 8).
    *    In all *other* cases (mixed neighbors, fewer than 7 azure neighbors, etc.), the azure pixel *is changed* to gray (color code 5).

4.  **Output:** The output grid maintains the same dimensions as the input grid. Only the colors of specific azure pixels are modified according to the rules above. All other pixels remain unchanged.
"""

import numpy as np

def count_neighbors(grid, row, col, target_color):
    """Counts the number of neighbors with a specific color."""
    height, width = grid.shape
    count = 0
    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i, j) != (row, col) and grid[i, j] == target_color:
                count += 1
    return count

def transform(input_grid):
    # Initialize the output grid as a copy of the input.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel.
    for row in range(height):
        for col in range(width):
            # Check if the current pixel is azure.
            if input_grid[row, col] == 8:
                # Count azure neighbors.
                azure_neighbors = count_neighbors(input_grid, row, col, 8)
                total_neighbors = 0
                for i in range(max(0, row - 1), min(height, row + 2)):
                    for j in range(max(0, col-1), min(width, col + 2)):
                        if (i,j) != (row, col):
                            total_neighbors +=1

                # Apply the conditional color change rules.
                if azure_neighbors == 8:
                    output_grid[row, col] = 5  # All neighbors azure: change to gray.
                elif azure_neighbors == 7 and total_neighbors == 8:
                     output_grid[row,col] = 8
                else:
                    output_grid[row, col] = 5  # Other cases: change to gray.

    return output_grid