import numpy as np

"""
Analyzes a 3x3 input grid containing 0s and 2s.
Determines if the pattern formed by the '2's exhibits horizontal, vertical, main diagonal, or anti-diagonal symmetry.
Returns 1 if any of these symmetries are present.
Returns 7 if none of these symmetries are present.
"""

def check_horizontal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the middle row."""
    # Compare the top row with the bottom row
    return grid[0] == grid[2]

def check_vertical_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the middle column."""
    # Compare the first column with the third column
    for i in range(3):
        if grid[i][0] != grid[i][2]:
            return False
    return True

def check_main_diagonal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the main diagonal (top-left to bottom-right)."""
    # Compare grid[i][j] with grid[j][i]
    for i in range(3):
        for j in range(i + 1, 3): # Only need to check one side of the diagonal
            if grid[i][j] != grid[j][i]:
                return False
    return True

def check_anti_diagonal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the anti-diagonal (top-right to bottom-left)."""
    # Compare grid[i][j] with grid[2-j][2-i]
    # Element (0,0) vs (2,2)
    if grid[0][0] != grid[2][2]:
        return False
    # Element (0,1) vs (1,2)
    if grid[0][1] != grid[1][2]:
        return False
    # Element (1,0) vs (2,1)
    if grid[1][0] != grid[2][1]:
        return False
    # Element (0,2) vs (0,2) - self compare
    # Element (1,1) vs (1,1) - self compare
    # Element (2,0) vs (2,0) - self compare
    # Can simplify the check by only comparing elements across the anti-diagonal
    if grid[0][0] != grid[2][2]: return False
    if grid[0][1] != grid[1][2]: return False
    #if grid[0][2] != grid[0][2]: return False # Always true
    if grid[1][0] != grid[2][1]: return False
    #if grid[1][1] != grid[1][1]: return False # Always true
    #if grid[2][0] != grid[2][0]: return False # Always true
    return True


def transform(input_grid: list[list[int]]) -> int:
    """
    Transforms the input grid based on symmetry properties.

    Args:
        input_grid: A 3x3 list of lists containing 0s and 2s.

    Returns:
        1 if the pattern of 2s has horizontal, vertical, main diagonal,
          or anti-diagonal symmetry.
        7 otherwise.
    """

    # Check for horizontal symmetry
    if check_horizontal_symmetry(input_grid):
        return 1

    # Check for vertical symmetry
    if check_vertical_symmetry(input_grid):
        return 1

    # Check for main diagonal symmetry
    if check_main_diagonal_symmetry(input_grid):
        return 1

    # Check for anti-diagonal symmetry
    if check_anti_diagonal_symmetry(input_grid):
        return 1

    # If none of the symmetries are found
    return 7