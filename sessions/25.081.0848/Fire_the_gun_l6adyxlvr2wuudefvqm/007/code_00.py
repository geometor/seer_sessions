"""
1.  **Identify Target Pixels:** Examine each pixel in the input grid. Focus on pixels with a value of '0' (white).
2.  **Count Adjacent Gray Pixels:** For each white pixel, count the number of directly adjacent pixels (up, down, left, right, *and diagonally*) that have a value of '5' (gray).
3.  **Conditional Color Change:** If a white pixel has *at least* two adjacent gray pixels, change the pixel's value to '2' (red) in the output grid.  It does not matter where the gray pixels are.
4.  **Copy Unchanged Pixels:** If a white pixel does not meet the condition (less than two adjacent gray pixels), its value remains '0' (white) in the output grid. All non-white pixels are copied to the output grid unchanged.
"""

import numpy as np

def count_adjacent_gray(grid, row, col):
    """Counts adjacent gray pixels (including diagonals)."""
    rows, cols = grid.shape
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and grid[i, j] == 5:
                count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the adjacency rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is white (0)
            if input_grid[row, col] == 0:
                # Count adjacent gray (5) pixels
                adjacent_gray_count = count_adjacent_gray(input_grid, row, col)
                # Change to red (2) if at least two adjacent gray pixels
                if adjacent_gray_count >= 2:
                    output_grid[row, col] = 2

    return output_grid