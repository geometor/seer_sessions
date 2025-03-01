"""
Transforms a grid with sparse red pixels into a grid with nested red squares.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a nested squares pattern of red pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid with the nested squares pattern.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)  # Initialize output grid with white pixels

    # Iterate to draw nested squares
    for size in range(min(rows, cols), 0, -2):
        top = (rows - size) // 2
        left = (cols - size) // 2
        bottom = top + size -1
        right = left + size -1

        # Draw square outline
        for i in range(left, right + 1):
          output_grid[top,i] = 2
          output_grid[bottom,i] = 2
        for i in range(top, bottom + 1):
          output_grid[i,left] = 2
          output_grid[i,right] = 2

    return output_grid