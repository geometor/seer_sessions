"""
The algorithm extracts a contiguous, non-white colored region from a larger grid. The extracted region maintains the relative positions and colors of its pixels. The output grid is a minimal bounding box around the extracted region. Background (white/0) pixels are discarded.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the smallest rectangular subgrid containing all non-white pixels.
    """
    rows, cols = input_grid.shape
    non_white_pixels = []

    # Find all non-white pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_white_pixels.append((r, c))

    if not non_white_pixels:  # Handle the case where the input is all white
        return np.array([[]])

    # Find bounding box coordinates
    min_row, min_col = non_white_pixels[0]
    max_row, max_col = non_white_pixels[0]
    for r, c in non_white_pixels:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # Create output grid
    output_rows = max_row - min_row + 1
    output_cols = max_col - min_col + 1
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy pixels to the output grid
    for r, c in non_white_pixels:
        output_grid[r - min_row, c - min_col] = input_grid[r, c]

    return output_grid