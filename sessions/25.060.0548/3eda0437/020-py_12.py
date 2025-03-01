"""
1.  **Iterate through Rows:** For each row in the input grid:
2.  **Find Outermost Blue Pixels:** Find the index of the first and the last blue pixel (value '1') in the current row.
3.  **Conditional Replacement:** If both a first and last blue pixel were found (i.e., there are at least two blue pixels in the row), iterate through the pixels *between* these two indices (exclusive of the blue pixels themselves).
4.  **Change White to Magenta:** Within this range, change any white pixel (value '0') to magenta (value '6').
5.  **Output:** The resulting grid after processing all rows is the output.
"""

import numpy as np

def find_outermost_blue(row):
    """Finds the indices of the first and last blue pixels in a row."""
    blue_indices = np.where(row == 1)[0]
    if len(blue_indices) >= 2:
        return blue_indices[0], blue_indices[-1]
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    rows, _ = input_grid.shape

    for r in range(rows):
        row = input_grid[r]
        first_blue, last_blue = find_outermost_blue(row)

        # Conditional replacement: only if at least two blue pixels exist
        if first_blue is not None and last_blue is not None:
            for c in range(first_blue + 1, last_blue):
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 6

    return output_grid