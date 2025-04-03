import numpy as np

"""
Identify the contiguous horizontal segment of non-white pixels in the input row. 
Keep only the first and last pixels of this segment, changing all pixels 
between them to white (0). All other white pixels remain unchanged.
"""

def find_non_white_segment(row):
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white segment in a 1D list (row).

    Args:
        row: A list of integers representing a row in the grid.

    Returns:
        A tuple (start_index, end_index, color) if a segment is found,
        otherwise returns (None, None, None).
    """
    start_index = -1
    end_index = -1
    segment_color = 0
    width = len(row)

    for i in range(width):
        if row[i] != 0: # Found a non-white pixel
            if start_index == -1: # First non-white pixel of the segment
                start_index = i
                segment_color = row[i]
            end_index = i # Update end_index for every non-white pixel in the potential segment
        elif start_index != -1: # Found a white pixel after starting a segment
            # Assuming only one segment per row based on examples
            break 
            
    if start_index != -1:
        return start_index, end_index, segment_color
    else:
        return None, None, None

def transform(input_grid):
    """
    Transforms the input grid according to the rule: keep only the endpoints
    of the single non-white horizontal segment.

    Args:
        input_grid: A list of lists representing the input grid. 
                      Expected to be a single row.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is treated as numpy array for easier handling if needed,
    # but list operations are sufficient here.
    input_row = input_grid[0]
    width = len(input_row)
    
    # Initialize output_grid as a single row of white pixels
    output_row = [0] * width

    # Find the non-white segment in the input row
    start_index, end_index, segment_color = find_non_white_segment(input_row)

    # If a segment was found, place its endpoints in the output row
    if start_index is not None:
        # Set the start pixel
        output_row[start_index] = segment_color
        # Set the end pixel (handles segments of length 1 correctly)
        output_row[end_index] = segment_color
        
    # Return the output row wrapped in a list to match grid format
    return [output_row]
