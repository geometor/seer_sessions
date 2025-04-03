"""
Identifies contiguous horizontal segments of orange pixels (7) in a 1D input grid (represented as 1xN).
Measures the length of each orange segment.
Replaces each orange segment with a segment of the same length and position, but with a color determined by the original segment's length according to the mapping: {1: maroon(9), 2: gray(5), 3: yellow(4)}.
White pixels (0) are preserved in their original positions. Orange segments with lengths other than 1, 2, or 3 remain unchanged (as orange).
"""

import numpy as np

# Helper function not strictly necessary for this simple case, but good practice.
# In this specific implementation, the logic is integrated directly into the main loop.

def transform(input_grid):
    """
    Transforms the input grid based on the lengths of contiguous orange segments.

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing a single list of integers.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    
    # Ensure input is valid and extract the single row
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, although ARC format is usually guaranteed.
        # Returning the input might be safer than an empty list if the cause of the previous error is unknown.
        return input_grid 
        
    input_row = np.array(input_grid[0])
    
    # Initialize the output row as a copy of the input row.
    # This preserves background (white) pixels and any orange segments
    # whose lengths do not match the specified mapping rules.
    output_row = input_row.copy()
    num_cols = len(input_row)

    # Define the mapping from orange segment length to the replacement color
    length_to_color_map = {
        1: 9,  # orange length 1 -> maroon
        2: 5,  # orange length 2 -> gray
        3: 4   # orange length 3 -> yellow
    }

    # Iterate through the columns to find orange segments
    col_index = 0
    while col_index < num_cols:
        # Check if the current pixel is orange (7)
        if input_row[col_index] == 7:
            # Found the start of a potential orange segment
            segment_start_col = col_index
            segment_length = 0
            
            # Measure the length of the contiguous orange segment
            # Keep track of current position within the segment scan
            current_scan_index = col_index
            while current_scan_index < num_cols and input_row[current_scan_index] == 7:
                segment_length += 1
                current_scan_index += 1 # Move scan index forward
            
            # Check if the measured length has a defined color mapping
            if segment_length in length_to_color_map:
                replacement_color = length_to_color_map[segment_length]
                # Fill the corresponding segment in the output row with the replacement color
                output_row[segment_start_col : segment_start_col + segment_length] = replacement_color
            # If length is not in the map (e.g., > 3 or 0), the segment remains orange
            # because the output_row was initialized as a copy of input_row.
            
            # Advance the main loop index past the processed segment
            col_index = current_scan_index 

        else:
            # If the pixel is not orange (it must be white based on examples),
            # simply move to the next column
            col_index += 1

    # Convert the final numpy row back into the list of lists format expected by ARC
    output_grid = [output_row.tolist()]
    
    return output_grid