import numpy as np
from typing import List, Tuple

"""
Identifies contiguous horizontal segments of non-white pixels in a 1D input grid (single row).
If a segment consists of a single pixel, it is expanded into a 3-pixel segment of the same color in the output grid, centered at the original pixel's location, respecting grid boundaries.
If a segment has a length greater than 1, it is copied directly to the output grid in the same position.
The background remains white (0). The output is returned as a NumPy array.
"""

def find_segments(row: List[int]) -> List[Tuple[int, int, int]]:
    """
    Finds contiguous segments of non-zero pixels in a 1D list.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A list of tuples, where each tuple represents a segment:
        (color, start_index, end_index).
    """
    segments = []
    start_index = -1
    current_color = 0
    for i, pixel in enumerate(row):
        if pixel != 0 and start_index == -1:
            # Start of a new segment
            start_index = i
            current_color = pixel
        elif pixel == 0 and start_index != -1:
            # End of the current segment (hit background)
            segments.append((current_color, start_index, i - 1))
            start_index = -1
            current_color = 0
        elif pixel != current_color and start_index != -1:
             # End of the current segment (color changed) - this task's examples don't show segments of different colors abutting
             # but handle it defensively.
            segments.append((current_color, start_index, i - 1))
            # Start of a new segment immediately
            start_index = i
            current_color = pixel

    # Check if a segment was ongoing at the end of the row
    if start_index != -1:
        segments.append((current_color, start_index, len(row) - 1))

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on segment lengths.

    Args:
        input_grid: A NumPy array representing the input grid (expected to be 1xN).

    Returns:
        A NumPy array representing the transformed output grid.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Handle empty or incorrectly shaped input
    if input_grid.size == 0 or input_grid.shape[0] != 1:
         # Or raise an error, depending on desired behavior for invalid input
        return np.array([[]], dtype=int)

    # Extract the single row and its width
    input_row = input_grid[0].tolist() # Convert to list for find_segments
    width = len(input_row)

    # Initialize output_row as a list filled with background color (0)
    output_row = [0] * width

    # Find all non-background segments in the input row
    segments = find_segments(input_row)

    # Iterate through the identified segments and apply transformation rules
    for color, start_index, end_index in segments:
        length = end_index - start_index + 1

        if length == 1:
            # Segment is a single pixel at index start_index
            center_index = start_index
            # Expand to 3 pixels centered at center_index, painting the output row
            for offset in [-1, 0, 1]:
                target_index = center_index + offset
                # Check if the target index is within the grid bounds
                if 0 <= target_index < width:
                    output_row[target_index] = color
        else:
            # Segment length is not 1, copy it directly to the output row
            for i in range(start_index, end_index + 1):
                 # Boundary check (defensive, should be correct from find_segments)
                if 0 <= i < width:
                    output_row[i] = color

    # Convert the output row list back into a NumPy array with the correct shape (1xN)
    output_grid = np.array([output_row])

    return output_grid