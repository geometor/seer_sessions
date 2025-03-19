"""
The transformation rule identifies contiguous regions of red (2) pixels in the input grid and replaces them with gray (5) pixels in the output grid. The output grid's dimensions match the bounding box of the red regions in the input, padded with zeros if necessary to avoid a single-pixel output. White (0) pixels are implicitly preserved by the initialization of the output as all zeros.
"""

import numpy as np

def get_bounding_box(grid, color):
    """Finds the bounding box of a color region."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """Transforms the input grid by replacing red regions with gray, preserving white."""

    input_grid = np.array(input_grid)
    bounding_box = get_bounding_box(input_grid, 2)

    if bounding_box is None:  # Handle cases with no red pixels
        return input_grid.tolist()

    min_row, max_row, min_col, max_col = bounding_box

    # Calculate output grid dimensions.
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize output grid with zeros (white).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replace red with gray within the bounding box.
    for r in range(output_height):
        for c in range(output_width):
            if input_grid[min_row + r, min_col + c] == 2:
                output_grid[r, c] = 5

    return output_grid.tolist()