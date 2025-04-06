import numpy as np
import copy # Although numpy handles copies well, explicit copy might be clearer in some steps if not using numpy

"""
1. Analyze Input: Receive the input grid I (size N x N). Identify the unique non-zero digit d present in the grid.
2. Initialize Pattern: Create a new empty grid P of the same dimensions as the input grid (N x N).
3. Process First Two Rows:
    * Copy row 1 of the input grid I to row 0 of the pattern grid P.
    * Copy row 0 of the input grid I to row 1 of the pattern grid P.
4. Process Remaining Rows: For each row index i from 2 up to N-1:
    * For each column index j from 0 up to N-1:
        * Examine the element I[i, j] in the input grid.
        * If I[i, j] is 0, set the corresponding element P[i, j] in the pattern grid to the non-zero digit d.
        * If I[i, j] is d, set the corresponding element P[i, j] in the pattern grid to 0.
5. Construct Output: Create the output grid (size 2N x 2N) by tiling the completed pattern grid P in a 2x2 arrangement. Place P in the top-left, top-right, bottom-left, and bottom-right quadrants of the output grid.
6. Return Output: Return the constructed 2N x 2N output grid.
"""

def _find_non_zero_digit(grid: np.ndarray) -> int:
    """Finds the unique non-zero digit in the grid."""
    for row in grid:
        for element in row:
            if element != 0:
                return element
    # Should not happen based on problem description, but good practice
    raise ValueError("No non-zero digit found in the input grid.")


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid according to the specified rules:
    - Swaps the first two rows.
    - Inverts digits (0 <-> non-zero) for rows from index 2 onwards.
    - Tiles the resulting pattern grid 2x2 to create the output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    n = input_array.shape[0]

    # 1. Analyze Input: Identify the non-zero digit 'd'
    non_zero_digit = _find_non_zero_digit(input_array)

    # 2. Initialize Pattern grid P
    pattern_grid = np.zeros_like(input_array)

    # 3. Process First Two Rows (swap row 0 and row 1)
    if n >= 1:
        pattern_grid[0, :] = input_array[1, :]
    if n >= 2:
        pattern_grid[1, :] = input_array[0, :]

    # 4. Process Remaining Rows (index 2 to N-1)
    if n > 2:
        for r in range(2, n):
            for c in range(n):
                if input_array[r, c] == 0:
                    pattern_grid[r, c] = non_zero_digit
                else: # it must be the non_zero_digit
                    pattern_grid[r, c] = 0

    # 5. Construct Output grid by tiling the pattern grid 2x2
    # Initialize output grid with size 2N x 2N
    output_n = 2 * n
    output_grid_np = np.zeros((output_n, output_n), dtype=int)

    # Tile the pattern_grid
    # Top-left quadrant
    output_grid_np[0:n, 0:n] = pattern_grid
    # Top-right quadrant
    output_grid_np[0:n, n:output_n] = pattern_grid
    # Bottom-left quadrant
    output_grid_np[n:output_n, 0:n] = pattern_grid
    # Bottom-right quadrant
    output_grid_np[n:output_n, n:output_n] = pattern_grid

    # Alternatively using np.tile:
    # output_grid_np = np.tile(pattern_grid, (2, 2))

    # 6. Return Output grid as list of lists
    output_grid = output_grid_np.tolist()

    return output_grid