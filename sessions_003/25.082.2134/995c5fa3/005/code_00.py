"""
1.  **Input:** A 4xN grid of single-digit integers (0-9).

2.  **Columnar Zero Analysis:** For each column of the input grid, count how many zeros (0s) it contains.

3. **Determine Start of Counting:** Scan from left to right, find the *fifth* column that contains at least one zero, and count from there.

4.  **Output Grid Generation (Row 1):**
    *   Starting from the column defined in step 3, count the number of columns to the *left* that contains *at least one* zero. If no such column exists, this count is zero.

5.  **Output Grid Generation (Row 2):**
    *    Starting from the column defined in step 3, count the number of columns, including the starting column, that contain *at least one* zero.

6.  **Output Grid Generation (Row 3):**
    *  Starting from the column defined in step 3, count the number of columns to the *right* (excluding the starting column) that contain *at least one* zero.

7.  **Output:** Construct a 3x3 grid where all elements in the first row are the same and equal to Row 1 result (mod 10), all elements in the second row are the same and equal to Row 2 result (mod 10), and all elements in the third row are the same equal to the Row 3 result (mod 10).
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
  count = 0
  for i in range(start_index):
    if zero_counts[i] > 0:
      count += 1
  return count

def count_right_with_zeros(grid, start_index):
    """Counts number of cols right of start that have at least one zero"""
    zero_counts = count_zeros_per_column(grid)
    count = 0
    for i in range(start_index + 1, len(zero_counts)):
        if zero_counts[i] > 0:
            count += 1
    return count

def count_including_and_right(grid, start_index):
    """Counts columns, including starting column, and to the right with zeros"""
    zero_counts = count_zeros_per_column(grid)
    count = 0
    for i in range(start_index, len(zero_counts)):
        if zero_counts[i] > 0:
          count += 1

    return count

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine Start of Counting
    start_column = find_fifth_zero_column(input_grid)
    if start_column == -1:
        return output_grid # Return all zeros if fewer than 5 zero columns

    # Output Grid Generation (Row 1)
    row1_count = count_left_with_zeros(input_grid, start_column)
    output_grid[0, :] = row1_count % 10

    # Output Grid Generation (Row 2)
    row2_count = count_including_and_right(input_grid, start_column)
    output_grid[1, :] = row2_count % 10

    # Output Grid Generation (Row 3)
    row3_count = count_right_with_zeros(input_grid, start_column)
    output_grid[2, :] = row3_count % 10

    return output_grid