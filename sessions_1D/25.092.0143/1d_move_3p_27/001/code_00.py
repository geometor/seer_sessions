import numpy as np

"""
1.  Initialize the output grid as a copy of the input grid, but filled entirely with the background color (white, 0).
2.  Iterate through the input grid from left to right (index 0 onwards) to identify the contiguous block of non-white pixels.
3.  Store the color and determine the length of this non-white block.
4.  Copy this identified non-white block into the output grid, starting at index 3 and maintaining its original length and color.
5.  Return the modified output grid.
"""

def find_colored_segment(grid_row):
    """
    Finds the first contiguous segment of non-white pixels in a 1D array.
    Returns the start index, length, and color of the segment, or None if no segment found.
    """
    segment_color = 0
    segment_start = -1
    segment_length = 0

    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-white pixel
            if segment_start == -1: # Start of a new segment
                segment_color = pixel
                segment_start = i
                segment_length = 1
            elif pixel == segment_color: # Continuation of the current segment
                segment_length += 1
            else: # Found a different color, stop (assuming only one segment)
                 break
        elif segment_start != -1: # Found white after starting a segment, segment ends
            break # Stop after the first segment

    if segment_start != -1:
        return segment_start, segment_length, segment_color
    else:
        return None, 0, 0 # No segment found


def transform(input_grid):
    """
    Shifts the first contiguous non-white segment found in the input grid 
    (assumed to be 1xN) three positions to the right in the output grid,
    filling the rest with white (0).
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)
    
    # Initialize output grid with the same shape as input, filled with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # Assuming the relevant data is always in the first row
    input_row = input_grid_np[0]
    
    # Find the colored segment in the input row
    start_index, length, color = find_colored_segment(input_row)

    # If a segment was found, copy it to the output grid, shifted by 3 positions
    if start_index is not None:
        output_start_index = 3 # Target start index in the output
        
        # Check if the shifted segment fits within the grid bounds
        if output_start_index + length <= output_grid.shape[1]:
            # Place the segment in the first row of the output grid
            output_grid[0, output_start_index : output_start_index + length] = color
        else:
            # Handle cases where the shifted segment would go out of bounds
            # Based on examples, this might not happen, or requires different logic.
            # For now, we'll just truncate, though this might be incorrect for other tasks.
             print(f"Warning: Shifted segment exceeds grid bounds. Truncating.")
             visible_length = output_grid.shape[1] - output_start_index
             if visible_length > 0:
                 output_grid[0, output_start_index : output_start_index + visible_length] = color


    return output_grid.tolist() # Return as a list of lists, standard ARC format