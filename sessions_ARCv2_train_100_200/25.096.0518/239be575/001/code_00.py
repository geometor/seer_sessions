import math
import numpy as np
from collections import Counter

"""
This function takes a 2D grid of integers as input.
It first checks if the grid is square (number of rows equals number of columns).
If the grid is square, the output is 0.
If the grid is not square, it searches for a 2x2 subgrid consisting entirely of the digit 2.
If such a 2x2 subgrid of 2s is found, the output is 8.
If the grid is not square and no 2x2 subgrid of 2s is found, the output is 0.
"""

def find_2x2_of_twos(grid: list[list[int]]) -> bool:
    """
    Searches the grid for any 2x2 subgrid containing only the digit 2.
    Returns True if found, False otherwise.
    """
    rows = len(grid)
    if rows < 2:
        return False
    cols = len(grid[0])
    if cols < 2:
        return False

    # Iterate through all possible top-left corners of a 2x2 subgrid
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the 2x2 subgrid starting at (r, c) consists only of 2s
            if (grid[r][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c+1] == 2 and
                grid[r+1][c+1] == 2):
                return True # Found the pattern
    return False # Pattern not found


def transform(input_grid: list[list[int]]) -> int:
    """
    Determines the output based on grid shape and presence of 2x2 blocks of '2'.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        An integer (0 or 8) based on the transformation rules.
    """
    # Get grid dimensions
    rows = len(input_grid)
    # Handle empty grid case gracefully although examples don't show it
    if rows == 0:
        return 0 
    cols = len(input_grid[0])
    if cols == 0:
        return 0

    # Check if the grid is square
    is_square = (rows == cols)

    # Apply transformation logic
    if is_square:
        # If the grid is square, the output is 0
        output_value = 0
    else:
        # If the grid is not square, check for the 2x2 pattern of 2s
        pattern_found = find_2x2_of_twos(input_grid)
        if pattern_found:
            # If the pattern is found, the output is 8
            output_value = 8
        else:
            # If the pattern is not found, the output is 0
            output_value = 0

    return output_value

# Helper function to parse the input string format if needed
# (assuming the main caller handles parsing based on the problem description)
def parse_input_string(input_str: str) -> list[list[int]]:
    """ Parses the multi-line string input into a list of lists of integers. """
    grid = []
    lines = input_str.strip().split('\n')
    for line in lines:
        grid.append([int(digit) for digit in line.split()])
    return grid
