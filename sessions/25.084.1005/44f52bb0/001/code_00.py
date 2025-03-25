"""
Accept a 3x3 input grid containing white (0) and red (2) pixels.
Determine if the pattern of red pixels exhibits any form of symmetry: vertical, horizontal, main diagonal, or anti-diagonal.
If any symmetry is detected, output the integer 1.
If no symmetry is detected across any of these axes, output the integer 7.
"""

import numpy as np

def is_vertically_symmetric(grid):
    """Checks if the grid is symmetric across the vertical centerline."""
    # Compare the first column with the last column
    return np.array_equal(grid[:, 0], grid[:, 2])

def is_horizontally_symmetric(grid):
    """Checks if the grid is symmetric across the horizontal centerline."""
    # Compare the first row with the last row
    return np.array_equal(grid[0, :], grid[2, :])

def is_main_diagonal_symmetric(grid):
    """Checks if the grid is symmetric across the main diagonal (top-left to bottom-right)."""
    # Compare the grid with its transpose
    return np.array_equal(grid, grid.T)

def is_anti_diagonal_symmetric(grid):
    """Checks if the grid is symmetric across the anti-diagonal (top-right to bottom-left)."""
    n = grid.shape[0] # Assuming square grid, n=3 here
    for r in range(n):
        for c in range(n):
            # Compare element [r, c] with element [n-1-c, n-1-r]
            if grid[r, c] != grid[n - 1 - c, n - 1 - r]:
                return False
    return True

def transform(input_grid):
    """
    Analyzes the symmetry of the input 3x3 grid and returns 1 if any symmetry
    (vertical, horizontal, main diagonal, anti-diagonal) is found, otherwise returns 7.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid)

    # Check for vertical symmetry
    if is_vertically_symmetric(grid):
        return 1

    # Check for horizontal symmetry
    if is_horizontally_symmetric(grid):
        return 1

    # Check for main diagonal symmetry
    if is_main_diagonal_symmetric(grid):
        return 1

    # Check for anti-diagonal symmetry
    if is_anti_diagonal_symmetric(grid):
        return 1

    # If none of the symmetries are found, return 7
    return 7