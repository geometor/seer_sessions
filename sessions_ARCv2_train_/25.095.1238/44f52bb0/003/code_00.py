"""
Analyzes a 3x3 NumPy array containing 0s and 2s for various types of symmetry 
based on the pattern formed by the '2's.
If the pattern exhibits horizontal, vertical, point (180-degree rotational), 
main diagonal, or anti-diagonal symmetry, the output is 1.
Otherwise, the output is 7.
"""

import numpy as np

# Helper function to check for horizontal symmetry
def has_horizontal_symmetry(grid: np.ndarray) -> bool:
    """Checks if the top row mirrors the bottom row."""
    return np.array_equal(grid[0,:], grid[2,:])

# Helper function to check for vertical symmetry
def has_vertical_symmetry(grid: np.ndarray) -> bool:
    """Checks if the left column mirrors the right column."""
    return np.array_equal(grid[:,0], grid[:,2])

# Helper function to check for point symmetry (180-degree rotation)
def has_point_symmetry(grid: np.ndarray) -> bool:
    """Checks if the grid remains the same after 180-degree rotation."""
    # Rotate the grid by 180 degrees (2 * 90 degrees)
    rotated_grid = np.rot90(grid, 2)
    return np.array_equal(grid, rotated_grid)

# Helper function to check for main diagonal symmetry (transpose)
def has_main_diagonal_symmetry(grid: np.ndarray) -> bool:
    """Checks if the grid is symmetric across the main diagonal (top-left to bottom-right)."""
    return np.array_equal(grid, grid.T)

# Helper function to check for anti-diagonal symmetry
def has_anti_diagonal_symmetry(grid: np.ndarray) -> bool:
    """Checks if the grid is symmetric across the anti-diagonal (top-right to bottom-left)."""
    # Calculate the anti-transpose: transpose then flip left-right and up-down
    anti_transpose = np.fliplr(np.flipud(grid.T))
    # Alternatively: np.rot90(np.fliplr(grid), 1) or np.flipud(np.rot90(grid,1))
    return np.array_equal(grid, anti_transpose)


def transform(input_grid: np.ndarray) -> int:
    """
    Analyzes the symmetry of the pattern formed by '2's in a 3x3 input NumPy array.

    Args:
        input_grid: A 3x3 NumPy array containing integers 0 and 2.

    Returns:
        1 if any specified symmetry (horizontal, vertical, point, main diagonal, 
        anti-diagonal) is found, 7 otherwise.
    """

    # Check for horizontal symmetry
    if has_horizontal_symmetry(input_grid):
        return 1

    # Check for vertical symmetry
    if has_vertical_symmetry(input_grid):
        return 1

    # Check for point symmetry (180-degree rotation)
    if has_point_symmetry(input_grid):
        return 1

    # Check for main diagonal symmetry (transpose)
    if has_main_diagonal_symmetry(input_grid):
        return 1
        
    # Check for anti-diagonal symmetry
    if has_anti_diagonal_symmetry(input_grid):
         return 1

    # If none of the symmetry checks passed, return 7
    return 7
