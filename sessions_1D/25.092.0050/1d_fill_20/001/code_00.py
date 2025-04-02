"""
Identifies the two non-white pixels in a 1D input grid. 
Fills the segment between these two pixels (inclusive) with their color. 
Pixels outside this segment remain white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Fills the segment between two identical non-white marker pixels in a 1D grid.

    Args:
        input_grid (list): A list representing the 1D input grid (e.g., [0, 0, 7, 0, 0, 7, 0]).

    Returns:
        list: A list representing the transformed 1D output grid.
    """
    # Convert the input list to a NumPy array for easier processing
    # Assuming the input is always a single list representing the row
    grid = np.array(input_grid)

    # Find the non-white color
    # We expect only one non-white color besides 0 (white)
    non_white_colors = np.unique(grid[grid != 0])
    if len(non_white_colors) != 1:
        # Handle potential errors or unexpected inputs, though ARC examples are consistent
        # For this task, we assume exactly one non-white color marking the ends
        print(f"Warning: Expected exactly one non-white color, found {non_white_colors}")
        # As a fallback, just pick the first one if multiple exist, or handle as error
        if len(non_white_colors) == 0:
            return input_grid # No markers, return original
        marker_color = non_white_colors[0]
    else:
        marker_color = non_white_colors[0]

    # Find the indices (positions) of the marker color
    # np.where returns a tuple of arrays, one for each dimension
    # Since it's 1D, we take the first element of the tuple
    marker_indices = np.where(grid == marker_color)[0]

    if len(marker_indices) != 2:
        # Handle cases where there aren't exactly two markers
        # For this task, we assume exactly two markers
        print(f"Warning: Expected exactly two markers of color {marker_color}, found {len(marker_indices)}")
        # Fallback: if only one marker, maybe return original? Or fill just that spot?
        # Based on examples, we expect two. Return original if assumption fails.
        return input_grid

    # Determine the start and end indices of the segment to fill
    start_index = np.min(marker_indices)
    end_index = np.max(marker_indices)

    # Create the output grid as a copy of the input grid
    output_grid = grid.copy()

    # Fill the range from start_index to end_index (inclusive) with the marker color
    output_grid[start_index : end_index + 1] = marker_color

    # Convert the NumPy array back to a list before returning
    return output_grid.tolist()
