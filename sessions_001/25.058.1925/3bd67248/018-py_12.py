"""
Transforms an input grid based on the presence and location of a leftmost azure column.

1. Identifies the leftmost column containing only '8' (azure).
2. If found:
    a. Creates a diagonal line of '2' (red) from the top row, at the same column index as the azure column, down to the bottom-left.
    b. Replaces the entire bottom row with '4' (yellow).
3. If not found, returns the input grid unchanged.
"""

import numpy as np

def find_leftmost_azure_column(grid):
    """Finds the index of the leftmost column containing only '8' (azure)."""
    rows, cols = grid.shape
    for j in range(cols):
        is_azure_column = True
        for i in range(rows):
            if grid[i, j] != 8:
                is_azure_column = False
                break
        if is_azure_column:
            return j
    return -1  # Return -1 if no such column is found


def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the leftmost azure column
    azure_column_index = find_leftmost_azure_column(output_grid)

    # Conditional transformations
    if azure_column_index != -1:
        # Create red diagonal
        for i in range(rows):
            if azure_column_index - i >= 0:
                output_grid[i, azure_column_index - i] = 2

        # Fill bottom row with yellow
        output_grid[rows - 1, :] = 4
    else:
        # no change
        output_grid = np.copy(input_grid)

    return output_grid