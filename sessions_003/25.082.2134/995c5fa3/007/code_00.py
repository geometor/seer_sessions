"""
1.  **Input:** A grid (2D array) of single-digit integers (0-9).

2.  **Columnar Zero Analysis:** For each column of the input grid, count the number of zeros (cells with the value 0).

3.  **Determine Start Column:** Scan the columns of the input grid from left to right. Find the fifth column that contains at least one zero. Record the index of this column as `start_column`. If fewer than five columns contain zeros, the output is a 3x3 grid of all zeros.

4.  **Calculate Counts (if start_column exists):**
    *   `left_count`: Count the number of columns to the *left* of the `start_column` that contain at least one zero.
    *   `including_count`: Count the number of columns from the `start_column` to the *end* of the grid (inclusive) that contain at least one zero.
    *   `right_count`: Count the number of columns to the *right* of the `start_column` that contain at least one zero.

5.  **Output Grid Generation:**
    * Create a 3x3 output grid.
    * Set all elements of the first row to (`left_count` mod 10).
    * Set all elements of the second row to (`including_count` mod 10).
    * Set all elements of the third row to (`right_count` mod 10).

6.  **Output:** The 3x3 grid.
"""

import numpy as np

def count_zeros_per_column(grid):
    """Counts the number of zeros in each column."""
    return [np.sum(grid[:, j] == 0) for j in range(grid.shape[1])]

def find_fifth_zero_column(grid):
    """Finds the index of the fifth column with at least one zero."""
    zero_counts = count_zeros_per_column(grid)
    count = 0
    for i, num_zeros in enumerate(zero_counts):
        if num_zeros > 0:
            count += 1
            if count == 5:
                return i
    return -1  # Return -1 if there aren't five columns with zeros

def count_left_with_zeros(grid, start_index):
    """Counts number of cols left of start that have at least one zero."""
    zero_counts = count_zeros_per_column(grid)
    return sum(1 for i in range(start_index) if zero_counts[i] > 0)

def count_including_and_right_with_zeros(grid, start_index):
    """Counts columns, including starting column, and to the right with zeros"""
    zero_counts = count_zeros_per_column(grid)
    return sum(1 for i in range(start_index, len(zero_counts)) if zero_counts[i] > 0)

def count_right_with_zeros(grid, start_index):
    """Counts number of cols right of start that have at least one zero"""
    zero_counts = count_zeros_per_column(grid)
    return sum(1 for i in range(start_index + 1, len(zero_counts)) if zero_counts[i] > 0)
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine Start Column
    start_column = find_fifth_zero_column(input_grid)

    # Handle fewer than 5 columns with zeros
    if start_column == -1:
        return output_grid

    # Calculate counts
    left_count = count_left_with_zeros(input_grid, start_column)
    including_count = count_including_and_right_with_zeros(input_grid, start_column)
    right_count = count_right_with_zeros(input_grid, start_column)

    # Populate the output grid
    output_grid[0, :] = left_count % 10
    output_grid[1, :] = including_count % 10
    output_grid[2, :] = right_count % 10

    return output_grid