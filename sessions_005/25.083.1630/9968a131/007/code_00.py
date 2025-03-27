"""
The transformation involves identifying diagonals within the grid and shifting the cell values along those diagonals based on whether the diagonal's offset is odd or even. Diagonals parallel to the main diagonal (from top-left to bottom-right) are considered. The main diagonal has an offset of 0, diagonals below have positive offsets, and those above have negative offsets. Odd-offset diagonals have their elements cyclically shifted down by one position, *without* wrapping at this stage. Even-offset diagonals remain unchanged. The crucial change is that the wrapping, which was previously implicit in the diagonal extraction, is now handled *explicitly* when placing elements back into the output grid.
"""

import numpy as np

def get_diagonal(input_grid, offset):
    """
    Retrieves the elements along a specified diagonal, *without* wrapping.
    Returns the elements, and unwrapped row/col indices.

    Args:
        input_grid: The 2D numpy array.
        offset: The offset from the main diagonal.
    """
    rows, cols = input_grid.shape
    diagonal = []
    row_indices = []
    col_indices = []
    for i in range(max(rows, cols)):
        row = i - max(0, offset)
        col = i + max(0, -offset)
        if 0 <= row < rows and 0 <= col < cols:
            diagonal.append(input_grid[row, col])
            row_indices.append(row)
            col_indices.append(col)
    return diagonal, row_indices, col_indices

def shift_diagonal(diagonal):
    """Shifts a list (representing a diagonal) by one position down, wrapping."""
    return [diagonal[-1]] + diagonal[:-1]

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all possible diagonal offsets
    for offset in range(-rows + 1, cols):
        # Get the original diagonal and its indices *without* wrapping
        original_diagonal, row_indices, col_indices = get_diagonal(input_grid, offset)

        # Shift the diagonal values based on offset parity
        if offset % 2 != 0:
            shifted_diagonal = shift_diagonal(original_diagonal)
        else:
            shifted_diagonal = original_diagonal

        # Update the output_grid with the shifted values, *now* applying wrapping
        for i in range(len(row_indices)):
            output_grid[row_indices[i] % rows, col_indices[i] % cols] = shifted_diagonal[i]

    return output_grid