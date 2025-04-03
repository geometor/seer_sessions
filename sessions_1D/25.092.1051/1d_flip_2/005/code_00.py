"""
Transforms a grid containing a single row by finding a contiguous segment of
non-white pixels (colors != 0). Within this segment, it moves the first pixel
to the end of the segment, shifting the remaining pixels in the segment one
position to the left. White pixels (color 0) outside the segment remain unchanged.
The input and output are expected to be lists of lists, even for a single row.
If no valid segment (contiguous, length >= 2) is found, the input is returned unchanged.
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

    # Check if there are at least two non-white pixels required for the swap
    if len(non_white_indices) < 2:
        return None

    # Find the potential start and end boundaries of the non-white pixels
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    # Verify that the non-white pixels form a single contiguous block
    # The number of non-white pixels found must equal the span they cover (inclusive)
    if len(non_white_indices) == (end_index - start_index + 1):
        return start_index, end_index
    else:
        # If non-white pixels are found but aren't contiguous, this rule doesn't apply
        return None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (expected to have one row).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Validate input format: must be a list containing at least one list (row)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         # Return input unchanged if format is unexpected or invalid
        return input_grid

    # Step 1: Identify the single row within the input grid.
    # Assuming the task always operates on the first row if multiple exist,
    # based on the examples provided.
    input_row_list = input_grid[0]
    input_row_array = np.array(input_row_list)

    # Step 5: Make a copy of the input row to serve as the output row.
    output_row_array = np.copy(input_row_array)

    # Step 2 & 3: Scan the row to find the contiguous non-white segment and its indices.
    segment_indices = find_non_white_segment(input_row_array)

    # Step 4: Check if a valid segment exists (contiguous, length >= 2).
    if segment_indices:
        start_index, end_index = segment_indices

        # Perform the transformation only if a valid segment was found

        # Step 6: Get the color of the pixel at the starting index i (single pixel).
        single_pixel_color = input_row_array[start_index]

        # Step 7: Get the sequence of colors from index i+1 to j (the block).
        # Slicing handles cases where the block might be just one pixel.
        block_pixels = input_row_array[start_index + 1 : end_index + 1]

        # Step 8: In the output row, place the "block" sequence into indices i through j-1.
        # The slice length on the left side automatically matches the block_pixels length.
        output_row_array[start_index : end_index] = block_pixels

        # Step 9: In the output row, place the color of the "single pixel" at index j.
        output_row_array[end_index] = single_pixel_color

    # If no valid segment was found, output_row_array remains a copy of input_row_array.

    # Step 10: Return the modified output row, formatted as a grid.
    # Convert the numpy array row back to a list
    output_row_list = output_row_array.tolist()
    # Wrap the row list in another list to match the required grid format
    output_grid = [output_row_list]

    return output_grid