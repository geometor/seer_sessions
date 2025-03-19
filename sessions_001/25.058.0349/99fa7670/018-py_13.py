"""
1.  **Identify Seed Pixels:** Find all pixels with a value of 8 (azure) or 5 (gray).
2.  **Azure Expansion:** For *each* azure pixel, change all pixels in its row to azure.
3.  **Gray Expansion:** For *each* gray pixel, independently:
    *   Iterate through all cells at or below the gray pixel's row and at or to the right of the gray pixel's column.
    *   For each cell being considered, check if *all* cells to its left (on the same row) are azure (8).
    *   If the check in the previous step is true, change the cell's value to gray (5).
    *   If not, *do not* change the cell as part of this gray pixel's expansion.
"""

import numpy as np

def find_seed_pixels(grid, colors):
    """Finds the coordinates of pixels with specified colors in the grid."""
    seed_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel_value in enumerate(row):
            if pixel_value in colors:
                seed_pixels.append((row_index, col_index, pixel_value))
    return seed_pixels

def check_left_for_azure(grid, row, col):
    """Checks if all cells to the left of a given cell are azure (8)."""
    for c in range(col):
        if grid[row, c] != 8:
            return False
    return True

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find seed pixels for azure (8) and gray (5).
    seed_pixels = find_seed_pixels(input_grid, [8, 5])

    # Azure Expansion: Iterate through each seed pixel and expand azure horizontally.
    for row, col, value in seed_pixels:
        if value == 8:
            output_grid[row, :] = 8

    # Gray Expansion: Iterate through each gray seed pixel *independently*.
    gray_seeds = [(row, col) for row, col, value in seed_pixels if value == 5]
    for gray_row, gray_col in gray_seeds:
        # Iterate through cells below and to the right of the gray seed.
        for r in range(gray_row, output_grid.shape[0]):
            for c in range(gray_col, output_grid.shape[1]):
                # Check if all cells to the left are azure.
                if check_left_for_azure(output_grid, r, c):
                    output_grid[r, c] = 5

    return output_grid