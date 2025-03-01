"""
1.  **Input:** A 2D grid of numbers (input_grid).
2.  **Process:** For each row in the input_grid:
    *   Find the value of the element on the main diagonal (where the row index equals the column index).
    *   Create a new row in the output_grid where *all* elements have the same value as the diagonal element from the corresponding input row.
3.  **Output:** A new 2D grid (output_grid) where each row's elements are all equal to the corresponding diagonal element from the input_grid.
"""

import numpy as np

def get_diagonal_element(grid, row_index):
    """Gets the diagonal element for a given row."""
    return grid[row_index][row_index]

def transform(input_grid):
    """Transforms the input grid based on the diagonal elements."""
    input_grid = np.array(input_grid)  # Ensure numpy array for consistent handling
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]

    # initialize output_grid as a copy, we will modify it.
    output_grid = np.copy(input_grid)

    # change output pixels 
    for i in range(rows):
      diagonal_value = get_diagonal_element(input_grid, i)
      for j in range(cols):
        output_grid[i][j] = diagonal_value
    return output_grid