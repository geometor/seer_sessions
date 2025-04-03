"""
Shift a colored horizontal segment two steps to the right within a 1D grid.

1. Identify the contiguous horizontal segment of non-white pixels in the input row.
2. Determine the starting index, color, and length of this segment.
3. Calculate the new starting index by adding 2 to the original starting index.
4. Create a new output row of the same size, filled with white pixels.
5. Place the identified segment (with its original color and length) into the new output row starting at the calculated new position.
"""

import numpy as np

def find_segment(grid_row):
    """
    Finds the start index, end index, color, and length of the first contiguous 
    non-white segment in a 1D row.
    Returns None if no segment is found.
    """
    start_idx = -1
    segment_color = 0
    
    # Find the start of the segment
    for i, pixel in enumerate(grid_row):
        if pixel != 0:
            start_idx = i
            segment_color = pixel
            break
            
    if start_idx == -1:
        # No non-white segment found
        return None, None, None, None

    # Find the end of the segment
    end_idx = start_idx
    while end_idx + 1 < len(grid_row) and grid_row[end_idx + 1] == segment_color:
        end_idx += 1
        
    segment_length = end_idx - start_idx + 1
    
    return start_idx, end_idx, segment_color, segment_length

def transform(input_grid):
    """
    Transforms the input grid by shifting the horizontal colored segment 
    two positions to the right.
    
    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to have only one row for this task.
                                     
    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Assuming the input is effectively 1D, work with the first row
    input_row = np.array(input_grid[0])
    grid_width = len(input_row)

    # Initialize output_row with white pixels (0)
    output_row = np.zeros_like(input_row)

    # Find the segment in the input row
    start_idx, end_idx, segment_color, segment_length = find_segment(input_row)

    # If a segment was found, calculate its new position and draw it
    if start_idx is not None:
        # Calculate the new starting position (shift right by 2)
        new_start_idx = start_idx + 2
        new_end_idx = new_start_idx + segment_length - 1 # inclusive index

        # Ensure the new position is within bounds (although examples suggest it always is)
        if new_start_idx >= 0 and new_end_idx < grid_width:
            # Place the segment in the output row at the new position
            output_row[new_start_idx : new_end_idx + 1] = segment_color
        else:
            # Handle cases where the shift goes out of bounds, if necessary.
            # Based on examples, this shouldn't happen.
            # For safety, we could just return the initialized white grid or 
            # partially draw the segment if it clips the edge.
            # Sticking to the observed pattern: assume it fits.
             output_row[new_start_idx : new_end_idx + 1] = segment_color # allow numpy slicing to handle potential edge clip

    # Return the result as a 2D grid (list of lists)
    return [output_row.tolist()]
