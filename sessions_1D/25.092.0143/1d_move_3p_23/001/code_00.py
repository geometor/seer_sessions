"""
Identify the single contiguous horizontal segment of non-white pixels in the input row. 
Calculate the new starting position by adding 3 to the original starting index. 
Create a new output row of the same dimensions, filled with the background color (white, 0). 
Place the identified segment into the output row at the new calculated starting index, maintaining its original color and length.
"""

import numpy as np

def find_colored_segment(grid_row):
    """
    Finds the first contiguous segment of non-background (non-zero) color in a 1D array.

    Args:
        grid_row: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple (color, start_index, length) if a segment is found, otherwise None.
    """
    start_index = -1
    segment_color = 0
    length = 0

    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-background pixel
            if start_index == -1: # Start of a potential segment
                start_index = i
                segment_color = pixel
                length = 1
            elif pixel == segment_color: # Continuing the segment
                length += 1
            else: # Different color, segment ended before this
                break
        elif start_index != -1: # Found background after segment started
            break # Segment ended

    if start_index != -1:
        return segment_color, start_index, length
    else:
        return None # No segment found

def transform(input_grid):
    """
    Transforms the input grid by shifting the single colored segment 3 positions to the right.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected to be 1xN).

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Ensure input is treated as a 1D array for simplicity since all examples are 1xN
    input_row = input_grid[0]
    
    # Find the colored segment in the input row
    segment_info = find_colored_segment(input_row)

    if segment_info is None:
        # If no segment is found (e.g., all background), return a copy of the input
        # or handle as per specific requirements (here, assume return background).
        return np.zeros_like(input_grid)

    segment_color, start_index, length = segment_info

    # Calculate the new starting index for the segment
    new_start_index = start_index + 3

    # Initialize the output grid with the background color (0)
    output_grid = np.zeros_like(input_grid)
    output_row = output_grid[0] # Get the single row of the output

    # Check boundaries: ensure the shifted segment fits within the grid
    # This implementation assumes the shift is always valid based on examples,
    # but a robust solution might need explicit boundary checks.
    # Example check: if new_start_index + length > output_row.shape[0]: handle error or clip

    # Place the segment into the output row at the new position
    # Ensure indices are within bounds before slicing
    end_index = new_start_index + length
    if new_start_index < output_row.shape[0] and end_index <= output_row.shape[0]:
         output_row[new_start_index:end_index] = segment_color
    # else: handle cases where segment goes out of bounds if necessary

    return output_grid