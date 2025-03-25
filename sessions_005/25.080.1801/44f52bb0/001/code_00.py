"""
Counts red pixels in each row and column of a 3x3 grid.
If all row and column counts are odd, output is 1. Otherwise, output is 7.
"""

import numpy as np

def _count_red_pixels_per_row_and_col(grid):
    """Counts red pixels (value 2) in each row and column."""
    row_counts = []
    col_counts = []
    for i in range(3):
        row_count = 0
        col_count = 0
        for j in range(3):
            if grid[i][j] == 2:
                row_count += 1
            if grid[j][i] == 2:
                col_count += 1
        row_counts.append(row_count)
        col_counts.append(col_count)
    return row_counts, col_counts

def _all_odd(counts):
    """Checks if all numbers in a list are odd."""
    for count in counts:
        if count % 2 == 0:
            return False
    return True

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Count red pixels in each row and column.
    row_counts, col_counts = _count_red_pixels_per_row_and_col(input_grid)

    # Check if all row and column counts are odd.
    if _all_odd(row_counts) and _all_odd(col_counts):
        return 1
    else:
        return 7