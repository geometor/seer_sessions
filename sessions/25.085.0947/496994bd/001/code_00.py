import numpy as np

"""
Receives an input grid.
Identifies the contiguous block of rows starting from the top (row 0) that contain at least one non-white pixel (colors 1-9). Let the height of this block be 'k'.
Creates an output grid initially as a copy of the input grid.
Copies the rows of the identified top block from the input grid, in reverse order, to the bottom 'k' rows of the output grid. Specifically, input row 'i' (where 0 <= i < k) is copied to output row 'H - 1 - i', where 'H' is the total height of the grid.
"""

def _find_top_block_height(grid):
    """
    Finds the height of the block of rows starting from the top
    that contain at least one non-white pixel.
    """
    height = grid.shape[0]
    top_block_height = 0
    for r in range(height):
        # Check if the row contains any non-white pixel
        if np.any(grid[r] != 0):
            top_block_height = r + 1
        else:
            # First all-white row encountered, stop searching
            break
    # Handle case where the entire grid might be non-white
    # In this case, the loop completes, and top_block_height correctly reflects the grid height if the last row was non-white,
    # or the index of the first all-white row if one existed.
    # If the first row itself is all white, height will be 0, which is correct.
    return top_block_height

def transform(input_grid):
    """
    Transforms the input grid by mirroring the top non-white block of rows
    to the bottom of the grid, while keeping the original block at the top.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)

    # Find the height of the top block (k)
    k = _find_top_block_height(input_np)

    # If k > 0, there is a block to mirror
    if k > 0:
        # Iterate through the rows of the top block (indices 0 to k-1)
        for i in range(k):
            # Get the source row from the input grid
            source_row = input_np[i]
            # Determine the destination row index in the output grid
            # This reverses the order of the source rows for the bottom placement
            destination_row_index = H - 1 - i
            # Copy the source row to the destination row in the output grid
            output_np[destination_row_index] = source_row

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
