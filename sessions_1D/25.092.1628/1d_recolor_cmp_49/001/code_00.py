"""
Transforms the input grid by identifying all contiguous horizontal segments of red (2) pixels. 
It finds the maximum length among these segments. Then, it changes the color of all red segments 
that have this maximum length to orange (7). All other pixels (white pixels and red pixels 
in shorter segments) remain unchanged.
"""

import numpy as np

def find_segments(row, target_color):
    """
    Finds contiguous segments of a specific color in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing a grid row.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              in the format (start_index, length). Returns an empty list
              if no segments are found.
    """
    segments = []
    in_segment = False
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color and not in_segment:
            # Start of a new segment
            in_segment = True
            start_index = i
        elif pixel != target_color and in_segment:
            # End of the current segment
            in_segment = False
            segments.append((start_index, i - start_index))
    
    # Handle segment that goes to the end of the row
    if in_segment:
        segments.append((start_index, len(row) - start_index))
        
    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list containing a single list (representing a 1D row) 
                           with integer color values.

    Returns:
        list: A list containing a single list representing the transformed grid row.
    """
    # Convert input to numpy array for easier processing
    # Assuming input_grid is always a list containing one list (one row)
    input_row = np.array(input_grid[0])
    
    # Initialize output_grid as a copy of the input
    output_row = input_row.copy()
    
    # Define colors
    red = 2
    orange = 7
    
    # 1. Find all contiguous segments of red pixels
    red_segments = find_segments(input_row, red)
    
    # If no red segments found, return the original grid
    if not red_segments:
        return [output_row.tolist()] # Return in the expected list-of-lists format

    # 2. Calculate the length of each red segment (already done in find_segments)
    # 3. Determine the maximum length found among all red segments
    max_length = 0
    for _, length in red_segments:
        if length > max_length:
            max_length = length
            
    # 4. Create the output grid (already done by copying)
    # 5. Iterate through all identified red segments
    # 6. For segments with maximum length, change color from red to orange
    for start_index, length in red_segments:
        if length == max_length:
            # Change the color in the output grid for this segment
            output_row[start_index : start_index + length] = orange
            
    # 7. Leave all other pixels unchanged (already handled by copying initially)
    
    # 8. Return the modified output grid in the original list-of-lists format
    return [output_row.tolist()]
