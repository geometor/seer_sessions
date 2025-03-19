"""
1.  **Iterate Row-wise:** Process each row of the input grid independently.
2.  **Identify Separators (Per Row):** Within each row, find the column indices of all grey (5) pixels. These are the row's separators.
3.  **Handle No Separators:** If a row has no separators, replace all non-grey pixels in that row with azure (8).
4.  **Handle One Separator:** If a row has exactly one separator, replace all non-grey pixels to the left of the separator with azure (8) and all non-grey pixels to the right with maroon (9).
5.  **Handle Multiple Separators:** If a row has two or more separators:
    *   Replace all non-grey pixels to the left of the *first* separator in that row with azure (8).
    *   Replace all non-grey pixels between the *first* and *last* separator in that row with magenta (6).
    *   Replace all non-grey pixels to the right of the *last* separator in that row with maroon (9).
6.  **Preserve Separators:** Ensure that all grey (5) pixels remain unchanged in the output grid, regardless of their position.
"""

import numpy as np

def get_separator_indices_per_row(row, separator_color=5):
    """Finds the column indices of separator pixels within a single row."""
    return np.where(row == separator_color)[0]

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Iterate Row-wise
    for i in range(rows):
        row = input_grid[i]
        
        # 2. Identify Separators (Per Row)
        separator_indices = get_separator_indices_per_row(row)

        # 3. Handle No Separators
        if len(separator_indices) == 0:
            output_grid[i, row != 5] = 8
        # 4. Handle One Separator
        elif len(separator_indices) == 1:
            first_separator = separator_indices[0]
            output_grid[i, :first_separator] = 8
            output_grid[i, first_separator + 1:] = 9
            output_grid[i, first_separator] = 5 # keep separator
        # 5. Handle Multiple Separators
        else:
            first_separator = separator_indices[0]
            last_separator = separator_indices[-1]
            output_grid[i, :first_separator] = 8
            output_grid[i, first_separator + 1:last_separator] = 6
            output_grid[i, last_separator + 1:] = 9
            output_grid[i, separator_indices] = 5 # keep separators

    # 6. Preserve Separators (already handled in steps 3, 4 and 5)
    return output_grid