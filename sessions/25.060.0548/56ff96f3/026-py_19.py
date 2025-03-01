"""
1.  **Identify:** Locate all orange pixels (value 7) in the input grid.
2.  **Determine Shape and Expansion:**
    *   If the orange pixels form a contiguous shape, find the bounding rectangle that encompasses the entire orange shape.
    *   If the orange pixels form a line (horizontal or potentially others), find the row that is *two rows above* the topmost orange pixel.
    * Create a rectangle that starts at the found row, and matches the columns of the original orange pixels.

3. **Fill:**  Fill this determined rectangle with orange pixels in the output grid while keeping dimensions same.
"""

import numpy as np

def find_orange_pixels(grid):
    # Find coordinates of all orange pixels (value 7).
    orange_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 7:
                orange_pixels.append((row_index, col_index))
    return orange_pixels

def find_topmost_row(pixels):
    # Find the minimum row index among a set of pixels.
    if not pixels:
        return None
    min_row = pixels[0][0]
    for row, _ in pixels:
        min_row = min(min_row, row)
    return min_row

def transform(input_grid):
    # Initialize output grid with the same dimensions and default white pixels.
    output_grid = np.zeros_like(input_grid)

    # Find all orange pixels.
    orange_pixels = find_orange_pixels(input_grid)

    if not orange_pixels:
        return output_grid

    # Determine the topmost row of the orange pixels.
    topmost_row = find_topmost_row(orange_pixels)

    # Calculate the row two rows above the topmost orange pixel.
    start_row = max(0, topmost_row - 2)

    # Find min and max columns
    min_col = min(col for _, col in orange_pixels)
    max_col = max(col for _, col in orange_pixels)
    
    # Determine bottom row
    bottom_row = max(row for row, _ in orange_pixels)

    # Fill the rectangle with orange.
    for row in range(start_row, bottom_row + 1):
        for col in range(min_col, max_col + 1):
            output_grid[row, col] = 7

    return output_grid