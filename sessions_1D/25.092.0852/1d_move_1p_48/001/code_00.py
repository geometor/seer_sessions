import numpy as np

"""
Identifies a single contiguous horizontal segment of non-white pixels in a 
single-row input grid. Creates an output grid of the same dimensions, initially 
filled with white (0). Copies the identified segment into the output grid, shifted 
one position to the right, preserving its original color and length.
"""

def find_segment(row):
    """Finds the start index, end index, and color of the first contiguous non-white segment."""
    start_index = -1
    end_index = -1
    segment_color = 0  # Default to background color

    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Mark the start of the segment
                start_index = i
                segment_color = pixel
            end_index = i # Update the end index as long as we see the segment color
            # Check if the next pixel is different or end of row
            if i + 1 == len(row) or row[i+1] != segment_color:
                break # Segment ended
        elif start_index != -1: # We were in a segment, but now hit background
             break # Segment ended

    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, length, segment_color
    else:
        return None # No segment found


def transform(input_grid):
    """
    Shifts a single contiguous horizontal segment of non-white pixels 
    one position to the right within a single-row grid.

    Args:
        input_grid (list of lists): A grid representing the input state, 
                                     expected to have only one row.

    Returns:
        list of lists: A grid representing the output state with the segment shifted.
    """
    # Ensure input is treated as a single row
    # np.array makes manipulation easier
    input_row = np.array(input_grid[0])
    height = 1
    width = len(input_row)

    # Initialize output grid with background color (white = 0)
    output_row = np.zeros(width, dtype=int)

    # Find the non-white segment in the input row
    segment_info = find_segment(input_row)

    # If a segment is found, shift it right
    if segment_info:
        start_index, length, color = segment_info
        
        # Calculate the new starting position
        new_start_index = start_index + 1
        
        # Calculate the new ending position (exclusive)
        new_end_index = new_start_index + length

        # Check if the shifted segment fits within the grid boundaries
        if new_end_index <= width:
             # Place the segment in the output row at the new position
             output_row[new_start_index:new_end_index] = color
        # else:
            # If the segment goes out of bounds, it disappears (based on examples)
            # Since output_row is already zeros, nothing more needs to be done.
            # However, the examples show segments always fit after shifting.

    # Convert the output row back to the list of lists format
    output_grid = [output_row.tolist()]

    return output_grid