import copy

"""
Identifies contiguous horizontal segments of non-white pixels in a single-row input grid. 
For each segment found, it keeps the first and last pixel of the segment and changes 
all pixels strictly between the first and last pixel to white (0). 
Pixels outside the identified segment(s) remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists,
                                      expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid, also containing a single row.
    """
    # Ensure input is a list and not empty
    if not isinstance(input_grid, list) or not input_grid:
        return []
        
    # Extract the single row from the input grid
    # Assuming the input grid always has at least one row based on examples
    input_row = input_grid[0]
    
    # Create a copy of the input row to modify for the output
    # Using list() creates a shallow copy, sufficient for a list of integers
    output_row = list(input_row)
    
    # Initialize variables to track the current segment
    in_segment = False
    start_index = -1

    # Iterate through the input row to find and process segments
    for i, pixel in enumerate(input_row):
        # Check if we are entering a new non-white segment
        if pixel != 0 and not in_segment:
            in_segment = True
            start_index = i
            
        # Check if we are exiting a segment
        # This happens if we find a white pixel after being in a segment,
        # or if we reach the end of the row while in a segment.
        is_last_pixel = (i == len(input_row) - 1)
        if in_segment and (pixel == 0 or is_last_pixel):
            # Determine the end index of the segment
            # If the current pixel is white, the segment ended at the previous index (i-1)
            # If it's the last pixel and non-white, the segment ends here (i)
            end_index = (i - 1) if pixel == 0 else i
            
            # Apply the transformation: change inner pixels to white (0)
            # This modification only happens if the segment has length > 2
            # i.e., if end_index is at least 2 positions after start_index
            if end_index > start_index + 1:
                for j in range(start_index + 1, end_index):
                    output_row[j] = 0
                    
            # Reset segment tracking
            in_segment = False
            start_index = -1 # Not strictly necessary but good for clarity

    # Return the modified row, wrapped in a list to match ARC format
    return [output_row]
