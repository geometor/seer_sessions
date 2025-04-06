import numpy as np

"""
Checks a 3x3 grid containing 0s and 2s for various types of symmetry based on the pattern formed by the '2's.
If the pattern exhibits horizontal, vertical, point (180-degree rotational), main diagonal, or anti-diagonal symmetry, the output is 1.
Otherwise, the output is 7.
"""

# Helper function to check for horizontal symmetry
def has_horizontal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the top row mirrors the bottom row."""
    return grid[0] == grid[2]

# Helper function to check for vertical symmetry
def has_vertical_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the left column mirrors the right column."""
    return all(grid[i][0] == grid[i][2] for i in range(3))

# Helper function to check for point symmetry (180-degree rotation)
def has_point_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid remains the same after 180-degree rotation."""
    # Equivalent to checking grid[i][j] == grid[2-i][2-j] for all i, j
    rotated_grid = [row[::-1] for row in grid[::-1]]
    return grid == rotated_grid

# Helper function to check for main diagonal symmetry (transpose)
def has_main_diagonal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the main diagonal (top-left to bottom-right)."""
    # Equivalent to checking grid[i][j] == grid[j][i]
    return all(grid[i][j] == grid[j][i] for i in range(3) for j in range(i + 1, 3))

# Helper function to check for anti-diagonal symmetry
def has_anti_diagonal_symmetry(grid: list[list[int]]) -> bool:
    """Checks if the grid is symmetric across the anti-diagonal (top-right to bottom-left)."""
    # Equivalent to checking grid[i][j] == grid[2-j][2-i]
    return all(grid[i][j] == grid[2-j][2-i] for i in range(3) for j in range(3))


def transform(input_grid: list[list[int]]) -> int:
    """
    Analyzes the symmetry of the pattern formed by '2's in a 3x3 input grid.

    Args:
        input_grid: A 3x3 list of lists containing integers 0 and 2.

    Returns:
        1 if any specified symmetry (horizontal, vertical, point, diagonal) is found,
        7 otherwise.
    """

    # Check for horizontal symmetry
    if has_horizontal_symmetry(input_grid):
        return 1

    # Check for vertical symmetry
    if has_vertical_symmetry(input_grid):
        return 1

    # Check for point symmetry
    if has_point_symmetry(input_grid):
        return 1

    # Check for main diagonal symmetry
    # Note: Based on examples, horizontal/vertical/point seem sufficient,
    # but including diagonals as per the detailed NL program.
    if has_main_diagonal_symmetry(input_grid):
        return 1
        
    # Check for anti-diagonal symmetry
    if has_anti_diagonal_symmetry(input_grid):
         return 1

    # If no symmetry is found
    return 7