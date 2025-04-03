import numpy as np

"""
Identifies a single contiguous horizontal segment of non-white pixels in the 
input row and shifts this segment one position to the right in the output row. 
The background remains white (0). The dimensions, segment color, and segment 
length are preserved. Assumes the input is effectively a single row based on 
examples.
"""

def find_segment(row):
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white segment in a 1D numpy array (row).

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, segment_color) if a segment is found,
               otherwise (None, None, None). Returns the indices inclusive.
    """
    start_index = -1
    end_index = -1
    segment_color = 0
    width = len(row)

    for i, pixel in enumerate(row):
        # If we find a non-white pixel and haven't started a segment yet
        if pixel != 0 and start_index == -1:
            start_index = i
            segment_color = pixel
            end_index = i # Initialize end index
        # If we are in a segment (start_index != -1) and find the same color pixel
        elif start_index != -1 and pixel == segment_color:
             end_index = i # Update the end index
        # If we are in a segment and find a different pixel (white or other color)
        elif start_index != -1 and pixel != segment_color:
            # Segment ended just before this pixel
            break # Assume only one contiguous segment per row per problem description
            
    if start_index == -1: # No segment found
        return None, None, None
        
    return start_index, end_index, segment_color


def transform(input_grid):
    """
    Transforms the input grid by finding a single horizontal non-white segment 
    in the first row and shifting it one position to the right.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid. 
                                Assumed to be effectively 1D based on examples.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # Ensure input is treated as numpy array
    input_grid_np = np.array(input_grid)
    
    # Get dimensions - assuming operation mainly on the first row based on examples
    # If grid is empty or has no rows, return it as is (or handle as error)
    if input_grid_np.size == 0:
        return input_grid_np
        
    height, width = input_grid_np.shape
    
    # Initialize output grid with background color (white=0)
    # Using zeros_like preserves the original dtype and shape
    output_grid = np.zeros_like(input_grid_np)

    # Extract the first row (assuming the core logic applies here based on examples)
    # If multiple rows could have segments, this logic would need modification.
    input_row = input_grid_np[0]

    # Find the non-white segment in the row
    start_index, end_index, segment_color = find_segment(input_row)

    # Check if a segment was found
    if start_index is not None:
        # Calculate the new starting position (shifted right by 1)
        new_start_index = start_index + 1
        
        # Copy the segment to the new position in the output grid's first row
        for i in range(end_index - start_index + 1):
            current_input_col = start_index + i
            current_output_col = new_start_index + i
            
            # Ensure the target column index is within the grid bounds
            if current_output_col < width:
                # Place the pixel from the input segment into the output grid
                # Note: using segment_color ensures uniformity if needed, 
                # but copying input_row[current_input_col] is also valid here.
                output_grid[0, current_output_col] = segment_color
                
    # If input had multiple rows, but logic only applied to first,
    # the other rows in output_grid remain zeros. 
    # If the intent was to copy other rows, that needs to be added.
    # Based on examples, only first row seems relevant.

    return output_grid.tolist() # Return as list of lists per ARC standard