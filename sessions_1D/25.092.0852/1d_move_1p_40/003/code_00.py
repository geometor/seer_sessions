import numpy as np
import copy

def find_non_white_segment(grid_row):
    """
    Finds the start index, end index, and color of the first contiguous
    non-white segment in a 1D grid row.

    Args:
        grid_row (np.ndarray): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: A tuple containing (start_index, end_index, segment_color).
               Returns (None, None, None) if no non-white segment is found.
    """
    start_index = -1
    segment_color = -1
    
    # Find the start of the segment
    for i, color in enumerate(grid_row):
        if color != 0:
            start_index = i
            segment_color = color
            break
            
    # If no non-white pixel found, return None
    if start_index == -1:
        return None, None, None
        
    # Find the end of the segment
    end_index = start_index
    while end_index + 1 < len(grid_row) and grid_row[end_index + 1] == segment_color:
        end_index += 1
        
    return start_index, end_index, segment_color

def transform(input_grid):
    """
    Transforms the input grid by finding the first contiguous non-white segment 
    in the single row and shifting it one position to the right. The original 
    starting position of the segment becomes white (0).

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    # Input is expected as [[...]], so access the first element for the row data
    if not input_grid or not input_grid[0]:
         # Handle empty grid case
         return [] if not input_grid else [[]]
         
    input_np = np.array(input_grid[0], dtype=int)
    
    # Get grid dimensions (only width matters here)
    width = input_np.shape[0]
    
    # Initialize output_grid as a copy of the input row
    output_grid_row = np.copy(input_np)

    # Find the non-white segment
    start_index, end_index, segment_color = find_non_white_segment(input_np)

    # If a segment was found, apply the transformation
    if start_index is not None:
        # Set the original start position to white
        output_grid_row[start_index] = 0
        
        # Shift the segment one position to the right
        for i in range(start_index, end_index + 1):
            target_index = i + 1
            # Check if the target index is within the grid bounds
            if target_index < width:
                # Set the pixel at the target index to the segment's color
                output_grid_row[target_index] = segment_color
            # If target_index >= width, the pixel effectively shifts off the grid

    # Return the modified grid row wrapped in a list to match ARC format
    return [output_grid_row.tolist()]