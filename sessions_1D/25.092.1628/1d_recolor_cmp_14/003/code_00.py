"""
For each row in the input grid, identify the longest horizontal segment(s) 
of maroon (9) pixels and change their color to yellow (4). If multiple 
segments in a row share the maximum length for that row, change all of them.
Other pixels remain unchanged.
"""

import numpy as np
from typing import List, Tuple

def find_maroon_segments_in_row(row: np.ndarray) -> List[Tuple[int, int, int]]:
    """
    Identifies contiguous segments of maroon (9) pixels in a single row.

    Args:
        row: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of tuples, where each tuple represents a maroon segment
        and contains (start_col_index, end_col_index, length).
    """
    segments = []
    start_index = -1
    current_length = 0
    maroon_color = 9
    row_length = len(row)

    for i, pixel in enumerate(row):
        if pixel == maroon_color:
            # Start of a new segment or continuation of an existing one
            if start_index == -1:
                start_index = i
            current_length += 1
        else:
            # End of a segment (if one was active)
            if start_index != -1:
                segments.append((start_index, i - 1, current_length))
                # Reset segment tracking
                start_index = -1
                current_length = 0

    # Handle segment ending at the very end of the row
    if start_index != -1:
        segments.append((start_index, row_length - 1, current_length))

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    num_rows, _ = input_grid.shape
    yellow_color = 4

    # Iterate through each row of the grid
    for r in range(num_rows):
        current_row = input_grid[r, :]

        # Find all horizontal maroon segments in the current row
        maroon_segments = find_maroon_segments_in_row(current_row)

        # If no maroon segments found in this row, continue to the next row
        if not maroon_segments:
            continue

        # Find the maximum length among the segments in this row
        max_length_in_row = 0
        for _, _, length in maroon_segments:
            if length > max_length_in_row:
                max_length_in_row = length
        
        # If max_length is 0 (shouldn't happen if segments exist, but safe check)
        if max_length_in_row == 0:
             continue

        # Recolor the longest segments in the output grid for this row
        for start_col, end_col, length in maroon_segments:
            if length == max_length_in_row:
                # Change the color of pixels in this segment to yellow in the output grid
                output_grid[r, start_col : end_col + 1] = yellow_color

    # Return the modified grid
    return output_grid