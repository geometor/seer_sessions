"""
Transforms a 1xN input grid containing a single contiguous horizontal segment of a non-white color.
The output grid retains only the first and last pixels of this segment, preserving their original color.
All other pixels in the output grid are set to white (0).
If the input grid contains no non-white pixels, the output is an all-white grid of the same dimensions.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies the endpoints of a single non-white horizontal segment in a 1xN grid
    and returns a grid where only these endpoints retain the segment's color.

    Args:
        input_grid: A numpy array representing the input grid (expected shape [1, N]).

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_grid_np.shape

    # Initialize the output grid with the same dimensions as the input, filled with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # Find the indices (column indices) of all non-white pixels in the first row
    # Since the grid is 1xN, we only look at row 0
    non_white_indices = np.where(input_grid_np[0, :] != 0)[0]

    # Check if any non-white pixels were found
    if non_white_indices.size > 0:
        # Find the index of the first (leftmost) non-white pixel
        start_index = np.min(non_white_indices)
        # Find the index of the last (rightmost) non-white pixel
        end_index = np.max(non_white_indices)

        # Get the color of the segment (using the color of the first non-white pixel)
        segment_color = input_grid_np[0, start_index]

        # Set the pixel at the start_index in the output grid to the segment color
        output_grid[0, start_index] = segment_color
        # Set the pixel at the end_index in the output grid to the segment color
        output_grid[0, end_index] = segment_color

    # Return the modified output grid
    return output_grid.tolist() # Return as list of lists for compatibility
