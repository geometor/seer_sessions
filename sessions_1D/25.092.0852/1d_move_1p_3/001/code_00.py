"""
Identifies a single contiguous horizontal segment of non-white pixels in the input row.
Shifts this segment one position to the right in the output row, maintaining its color and length.
The background remains white (0).
"""

import numpy as np

def find_non_white_segment(grid_row):
    """
    Finds the start index, end index (inclusive), color, and length 
    of the first contiguous non-white segment in a 1D array.
    Returns None if no non-white segment is found.
    """
    start_idx = -1
    segment_color = -1
    segment_length = 0
    
    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-white pixel
            if start_idx == -1:  # Start of the segment
                start_idx = i
                segment_color = pixel
            segment_length += 1
        elif start_idx != -1: # End of the segment (found a white pixel after segment started)
            break # Since there's only one segment expected, we can stop

    if start_idx != -1:
        end_idx = start_idx + segment_length - 1
        return start_idx, end_idx, segment_color, segment_length
    else:
        return None # No segment found

def transform(input_grid):
    """
    Takes a 1xN grid (represented as a 1D list or array), finds the non-white
    segment, and returns a new grid of the same size with the segment
    shifted one position to the right.
    """
    # Ensure input is treated as a 1D array
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        # Handle case where input might be [[...]]
        grid_row = np.array(input_grid[0])
    elif isinstance(input_grid, np.ndarray) and input_grid.ndim > 1:
         # Handle case where input might be a 2D numpy array with 1 row
         grid_row = input_grid.flatten()
    else:
        grid_row = np.array(input_grid) # Assume it's already 1D or convertible

    # Find the segment in the input row
    segment_info = find_non_white_segment(grid_row)

    # Initialize output_grid with the same shape and background color (white)
    output_grid = np.zeros_like(grid_row)

    if segment_info:
        start_idx, end_idx, segment_color, segment_length = segment_info
        
        # Calculate the new starting position for the segment
        new_start_idx = start_idx + 1
        new_end_idx = new_start_idx + segment_length # Exclusive index for slicing

        # Check if the shift is valid (within bounds)
        if new_end_idx <= len(grid_row):
             # Place the shifted segment into the output grid
             output_grid[new_start_idx:new_end_idx] = segment_color
        else:
            # Handle potential out-of-bounds shift, though not expected based on examples
            # For now, just place what fits or return original/empty if needed
            # Based on examples, we assume it always fits.
             output_grid[new_start_idx:new_end_idx] = segment_color


    # Return the output grid, potentially reshaping if the original was 2D 1xN
    if isinstance(input_grid, np.ndarray) and input_grid.ndim == 2:
        return output_grid.reshape(1, -1)
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
         return [output_grid.tolist()] # Match [[...]] format
    else:
        return output_grid.tolist() # Return as a standard list if input was 1D list
