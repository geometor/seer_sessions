"""
1.  **Identify Target Pixels:** Examine each pixel in the input grid.
2.  **Check for color 8 (azure):**
    *   Iterate all pixels. If a pixel is color 8 (azure), check across the row and down the column of this pixel.
3.  **Conditional Replacement:** For any pixel found in step 2, that is any pixel that is on the same row, or in the same column with an 8 (azure) and is not a 2 (red):
    *   Change the target pixel's color to 5 (grey).
4.  **Other pixels are Unchanged.** All pixels that don't meet the condition in step 2 retain their original color.
5.  **Output:** The output grid contains the result of these replacements.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the row and column neighbors
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Check for color 8 (azure)
            if input_grid[r, c] == 8:
                # Check entire row and column for replacement
                for i in range(cols):
                    if output_grid[r,i] != 2:
                        output_grid[r, i] = 5  # Change to grey
                for j in range(rows):
                     if output_grid[j,c] != 2:
                        output_grid[j, c] = 5  # Change to grey
    return output_grid