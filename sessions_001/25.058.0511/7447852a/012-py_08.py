"""
Transforms an input grid by identifying white pixels (0) that are adjacent (horizontally, vertically, or diagonally) to red pixels (2) and changing those white pixels to yellow (4).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on red pixel adjacency.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is white
            if input_grid[r, c] == 0:
                # Check for adjacent red pixels
                is_adjacent_to_red = False
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        if (i != r or j != c) and input_grid[i, j] == 2:
                            is_adjacent_to_red = True
                            break  # Exit inner loop if a red pixel is found
                    if is_adjacent_to_red:
                        break  # Exit outer loop if a red pixel is found

                # Change to yellow if adjacent to a red pixel
                if is_adjacent_to_red:
                    output_grid[r, c] = 4

    return output_grid