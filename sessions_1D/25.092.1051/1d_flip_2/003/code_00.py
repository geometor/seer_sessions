"""
Transforms a grid containing a single row by finding a contiguous segment of
non-white pixels. Within this segment, it moves the first pixel to the end
of the segment, shifting the remaining pixels in the segment one position to the
left. White pixels outside the segment remain unchanged. The input and output
formats are lists of lists, even for a single row.
"""

import numpy as np

def find_non_white_segment(grid_row):
    """
    Finds the start and end indices of the contiguous non-white segment in a 1D array.

    Args:
        grid_row: A 1D numpy array representing a single row of the grid.

    Returns:
        A tuple (start_index, end_index) if a contiguous segment of at least
        two non-white pixels is found, otherwise None.
    """
    # Find indices of all non-white pixels (color != 0)
    non_white_indices = np.where(grid_row != 0)[0]

    # Check if there are at least two non-white pixels for the swap
    if len(non_white_indices) < 2:
        return None

    # Find the boundaries of the non-white pixels
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    # Verify that the non-white pixels form a single contiguous block
    # The number of non-white pixels must equal the span they cover
    if len(non_white_indices) == (end_index - start_index + 1):
        return start_index, end_index
    else:
        # If non-white pixels are found but aren't contiguous, this rule doesn't apply
        # based on the examples provided.
        return None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (expected to have one row).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Check if input is valid (list of lists, has at least one row)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         # Return input unchanged if format is unexpected
         # Or consider raising an error depending on requirements
        return input_grid

    # Extract the first row as a numpy array
    # Assuming the task always provides grids with at least one row based on examples
    input_row_array = np.array(input_grid[0])

    # Initialize the output row as a copy of the input row
    output_row_array = np.copy(input_row_array)

    # Find the contiguous non-white segment in the row
    segment_indices = find_non_white_segment(input_row_array)

    # If a valid segment is found, perform the transformation
    if segment_indices:
        start_index, end_index = segment_indices

        # Extract the color of the first pixel in the segment
        single_pixel_color = input_row_array[start_index]

        # Extract the colors of the remaining pixels in the segment (the block)
        # Slicing works correctly even if the block has only one pixel
        block_pixels = input_row_array[start_index + 1 : end_index + 1]

        # Place the block pixels into the output row, shifted one position left
        # The slice length automatically handles the size of the block
        output_row_array[start_index : end_index] = block_pixels

        # Place the single pixel's color at the end of the segment in the output row
        output_row_array[end_index] = single_pixel_color

    # Convert the transformed numpy row back to a list
    output_row_list = output_row_array.tolist()

    # Return the transformed row wrapped in a list to match the output format
    output_grid = [output_row_list]

    return output_grid