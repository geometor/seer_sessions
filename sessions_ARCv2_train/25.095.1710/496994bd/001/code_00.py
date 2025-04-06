"""
Identifies the contiguous block of rows starting from the top row (row 0) of the input grid that contain at least one non-zero element (TopBlock).
Determines the number of rows in TopBlock (N).
Creates an output grid initially identical to the input grid.
Creates a vertically mirrored copy of TopBlock (MirroredBlock).
Replaces the last N rows of the output grid with the rows from MirroredBlock.
"""

import copy

# Helper function to check if a row consists entirely of zeros
def _is_zero_row(row: list[int]) -> bool:
    """Checks if all elements in a list (row) are zero."""
    return all(cell == 0 for cell in row)

# Helper function to find the top block of non-zero rows
def _find_top_non_zero_block(grid: list[list[int]]) -> list[list[int]]:
    """Finds the contiguous block of rows from the top containing non-zeros."""
    top_block = []
    for row in grid:
        # Stop iterating if a row with only zeros is found
        if _is_zero_row(row):
            break
        top_block.append(row)
    return top_block

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by copying the top non-zero rows,
    and placing a vertically mirrored version of these rows at the bottom
    of the grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return [] # Handle empty grid case

    # 1. Identify the contiguous block of rows from the top (TopBlock)
    #    containing at least one non-zero element.
    top_block = _find_top_non_zero_block(input_grid)

    # 2. Determine the number of rows in TopBlock (N).
    n = len(top_block)

    # 3. Create a new grid, OutputGrid, with the same dimensions as the input grid.
    # 4. Copy all rows from the input grid to the OutputGrid.
    #    Using deepcopy ensures that subsequent modifications don't affect
    #    the original input or the top_block reference if needed later.
    output_grid = copy.deepcopy(input_grid)

    # Proceed only if there are non-zero rows to mirror (n > 0)
    # and the mirror fits within the grid height (n <= height)
    if n > 0 and n <= height:
        # 5. Create a reversed copy of the rows in TopBlock (MirroredBlock).
        #    Slicing [::-1] creates a reversed shallow copy of the list of rows.
        mirrored_block = top_block[::-1]

        # 6. Replace the last N rows of the OutputGrid with the rows from MirroredBlock.
        for i in range(n):
            # Calculate the target row index in the output grid
            # The first row of mirrored_block goes to output_grid[height - n]
            # The second row of mirrored_block goes to output_grid[height - n + 1]
            # ...
            # The last row (n-1) of mirrored_block goes to output_grid[height - 1]
            target_row_index = height - n + i

            # Assign the corresponding row from the mirrored block
            # We assign the row directly. Since mirrored_block was derived from
            # top_block which came from input_grid, and output_grid is a deepcopy,
            # this assignment is safe.
            output_grid[target_row_index] = mirrored_block[i]

    # 7. The final OutputGrid is the result.
    return output_grid