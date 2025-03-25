"""
Transforms an input grid of integers into an output grid based on the following rules:

1.  Check for Uniformity: If all cells in the input grid have the same value, create an output grid of the same dimensions. Fill the top row of the output grid with gray (5) and all other cells with white (0). Stop.

2.  If Not Uniform: If the input grid is not uniform, check the diagonals.

3.  Diagonal Check:
    *   Get both the main diagonal (top-left to bottom-right) and the anti-diagonal (top-right to bottom-left) of the input grid.
    *   If the main diagonal elements are all the same, create an output grid of the same size, fill the main diagonal with gray (5) and all other cells with white (0). Stop.
    *   If the main diagonal elements are *not* all the same, and the anti-diagonal elements are *not* all the same, check if there any common elements between the sets formed by elements of each diagonals.
        * If the sets formed by elements in the two diagonals do not intersect, then create an output grid of the same dimensions and fill the anti-diagonal with gray(5) and all other cells with white (0). Stop.
    *   Otherwise, the output is an all-white grid
"""

import numpy as np

def _check_uniformity(grid):
    """Checks if all cells in the grid have the same value."""
    return all(x == grid.flat[0] for x in grid.flat)

def _get_diagonals(grid):
    """Returns the main and anti-diagonals of the grid."""
    rows, cols = grid.shape
    main_diag = [grid[i, i] for i in range(min(rows, cols))]
    anti_diag = [grid[i, rows - 1 - i] for i in range(min(rows, cols))]
    return main_diag, anti_diag

def _check_diagonal_uniformity(diagonal):
    """Checks if all elements in a diagonal are the same."""
    return all(x == diagonal[0] for x in diagonal)

def _check_diagonals_all_different(diag1, diag2):
    set1 = set(diag1)
    set2 = set(diag2)
    return len(set1.intersection(set2)) == 0

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Check for Uniformity
    if _check_uniformity(input_grid):
        output_grid[0, :] = 5  # Fill top row with gray
        return output_grid.tolist()

    # If Not Uniform, Check Diagonals
    main_diag, anti_diag = _get_diagonals(input_grid)
    main_diag_uniform = _check_diagonal_uniformity(main_diag)
    anti_diag_uniform = _check_diagonal_uniformity(anti_diag)

    if main_diag_uniform:
        # Fill main diagonal with gray
        for i in range(min(rows, cols)):
            output_grid[i, i] = 5
    elif not main_diag_uniform and not anti_diag_uniform: # Added check for anti diag
        # check if main and anti diagonals are different
        if _check_diagonals_all_different(main_diag, anti_diag):
            # Fill anti-diagonal with gray
             for i in range(min(rows, cols)):
                output_grid[i, rows - 1 - i] = 5

    return output_grid.tolist()