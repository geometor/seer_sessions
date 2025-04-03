import numpy as np

"""
Transforms a 1xN grid by identifying a contiguous block of a single non-white color.
The output grid retains the color of the block only at its start and end column indices within the single row,
with all other pixels set to white (0). If the input is all white, the output is also all white.
Assumes the input is a 2D NumPy array with shape (1, N).
"""

def find_block_endpoints_and_color(grid_row: np.ndarray) -> tuple[int, int, int] | None:
    """
    Finds the start index, end index, and color of a contiguous non-white block
    in a 1D numpy array representing a single row of the grid.

    Args:
        grid_row: A 1D numpy array (e.g., input_grid[0]).

    Returns:
        A tuple (start_index, end_index, color) if a non-white block is found,
        otherwise None. Assumes only one contiguous block per row, as per examples.
    """
    # Find indices of all non-white pixels (value != 0)
    non_white_indices = np.where(grid_row != 0)[0]

    # If no non-white pixels are found, there's no block
    if len(non_white_indices) == 0:
        return None

    # The start index is the first non-white index found
    start_index = non_white_indices[0]
    # The end index is the last non-white index found
    end_index = non_white_indices[-1]

    # Get the color from the pixel at the start of the block
    block_color = grid_row[start_index]

    return start_index, end_index, block_color


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid (1xN NumPy array).
    Identifies a horizontal block of non-white color and keeps only its
    endpoints in the output grid.

    Args:
        input_grid: A 2D NumPy array with shape (1, N) representing the input grid.

    Returns:
        A 2D NumPy array with the same shape (1, N) representing the transformed grid.
    """
    # Verify the input grid has the expected shape (1 row)
    if input_grid.shape[0] != 1:
        raise ValueError("Input grid must have exactly one row.")

    # Extract the single row (as a 1D array for easier processing)
    # input_grid[0] gives the first (and only) row as a 1D array
    grid_row = input_grid[0]
    output_shape = input_grid.shape # Preserve original shape (1, N)

    # Initialize the output grid with the same shape as the input, filled with white (0)
    output_grid = np.zeros(output_shape, dtype=input_grid.dtype)

    # Find the start index, end index, and color of the non-white block in the row
    block_info = find_block_endpoints_and_color(grid_row)

    # If a block was found (i.e., block_info is not None)
    if block_info:
        start_index, end_index, block_color = block_info

        # Set the pixel at the start index in the output grid's row to the block color
        output_grid[0, start_index] = block_color

        # Set the pixel at the end index in the output grid's row to the block color
        # Note: If start_index == end_index (block length 1), this correctly colors only one pixel.
        output_grid[0, end_index] = block_color

    # Return the output grid (which is all zeros if no block was found)
    return output_grid