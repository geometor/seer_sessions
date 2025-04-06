import math
import numpy as np
from collections import Counter

"""
Transforms an input grid based on its shape, the count of 2x2 blocks of '2's, and the total count of '8's.

1. Determine the grid dimensions (rows and columns).
2. Check if the grid is square (rows == columns).
3. If the grid is square, the output is 0.
4. If the grid is not square:
   a. Count the number of occurrences of the 2x2 subgrid pattern [[2, 2], [2, 2]]. Let this be block_count.
   b. Count the total number of times the digit '8' appears in the grid. Let this be eight_count.
   c. Check if block_count is exactly 2 AND eight_count is NOT equal to 13.
   d. If both conditions in step 4c are true, the output is 8.
   e. Otherwise (if block_count is not 2, OR if eight_count is 13), the output is 0.
"""

def count_2x2_of_twos(grid: list[list[int]]) -> int:
    """
    Counts the number of (potentially overlapping) 2x2 subgrids containing only the digit 2.

    Args:
        grid: A list of lists representing the 2D grid of integers.

    Returns:
        The integer count of 2x2 subgrids made entirely of '2's.
    """
    rows = len(grid)
    # Handle edge cases: grid too small
    if rows < 2:
        return 0
    # Assuming rectangular grid based on parsing logic (or external guarantee)
    cols = len(grid[0]) if rows > 0 and grid[0] else 0
    if cols < 2:
        return 0

    count = 0
    # Iterate through all possible top-left corners of a 2x2 subgrid
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the 2x2 subgrid starting at (r, c) consists only of 2s
            if (grid[r][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c+1] == 2 and
                grid[r+1][c+1] == 2):
                count += 1 # Found a pattern
    return count

def count_digit(grid: list[list[int]], digit: int) -> int:
    """Counts the occurrences of a specific digit in the grid."""
    count = 0
    for row in grid:
        count += row.count(digit)
    return count

def transform(input_grid: list[list[int]]) -> int:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        An integer (0 or 8) based on the transformation rules.
    """
    # Get grid dimensions
    rows = len(input_grid)
    # Handle empty grid case gracefully
    if rows == 0:
        return 0
    cols = len(input_grid[0]) if input_grid and input_grid[0] else 0
    if cols == 0:
        return 0

    # Check if the grid is square
    is_square = (rows == cols)

    # Apply transformation logic based on shape
    if is_square:
        # If the grid is square, the output is 0
        output_value = 0
    else:
        # If the grid is not square, count the 2x2 pattern of 2s
        block_count = count_2x2_of_twos(input_grid)
        # Count the total number of 8s in the grid
        eight_count = count_digit(input_grid, 8)

        # Determine output based on the block count and eight count
        if block_count == 2 and eight_count != 13:
            # If exactly two blocks are found AND the count of 8s is not 13, output is 8
            output_value = 8
        else:
            # Otherwise (block count != 2 OR eight count == 13), output is 0
            output_value = 0

    # The output is a single integer
    return output_value