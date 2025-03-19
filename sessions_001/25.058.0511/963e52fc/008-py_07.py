"""
1.  **Identify the Pattern:** Locate the single horizontal line of non-white pixels in the input grid. This line consists of an alternating sequence of red (2) and green (3) pixels.

2.  **Determine the length of the Pattern:** In the input the length of the pattern is 7 pixels

3.  **Expansion:** Duplicate the entire identified pattern, appending it to the right end of the original pattern.

4.  **Output:** Create a new grid with the same height as the input but double the original pattern's width. Place combined pattern in the center row, and keep all other pixels as white (0).
"""

import numpy as np

def find_pattern_row(grid):
    # Find the row index containing the pattern (non-white pixels)
    for i, row in enumerate(grid):
        if np.any(row != 0):
            return i, row[row != 0]
    return None, None

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the pattern row and the pattern itself
    pattern_row_index, pattern = find_pattern_row(input_grid)

    # Create the output grid with expanded width
    output_width = len(pattern) * 2
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)

    # Duplicate and insert pattern
    extended_pattern = np.concatenate((pattern, pattern))

    output_grid[pattern_row_index, :len(extended_pattern)] = extended_pattern

    return output_grid.tolist()