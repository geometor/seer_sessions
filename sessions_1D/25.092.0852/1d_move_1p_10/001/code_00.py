import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule: Identify a single contiguous segment of non-white pixels 
in the input row. Shift this segment one position to the right in the output row, 
maintaining its color and length. Fill the remaining positions with white (0).
"""

def find_segment(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white segment in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A tuple (start_index, end_index, color) if a segment is found,
        otherwise None.
    """
    start_index = -1
    color = -1
    for i, pixel in enumerate(grid):
        if pixel != 0:
            start_index = i
            color = pixel
            break  # Found the start of the segment

    if start_index == -1:
        return None  # No segment found

    end_index = start_index
    for i in range(start_index + 1, len(grid)):
        if grid[i] == color:
            end_index = i
        else:
            break # End of the segment

    return start_index, end_index, color

def transform(input_grid: List[int]) -> List[int]:
    """
    Shifts the non-white segment in a 1D grid one position to the right.

    Args:
        input_grid: A list of integers representing the input 1D grid.

    Returns:
        A list of integers representing the transformed 1D grid.
    """
    # Initialize output grid with the same size as input, filled with white (0)
    output_grid = [0] * len(input_grid)

    # Find the non-white segment in the input grid
    segment_info = find_segment(input_grid)

    # If no segment is found, return the all-white grid (which is already output_grid)
    if segment_info is None:
        return output_grid

    start_index, end_index, color = segment_info
    segment_length = end_index - start_index + 1

    # Calculate the new starting position for the segment
    new_start_index = start_index + 1

    # Copy the segment to the new position in the output grid
    # Iterate through the length of the original segment
    for i in range(segment_length):
        # Calculate the target index in the output grid
        output_index = new_start_index + i
        # Check if the target index is within the grid bounds
        if 0 <= output_index < len(output_grid):
            output_grid[output_index] = color

    return output_grid