import numpy as np
import copy

"""
Transforms the input grid by finding the first contiguous non-white segment 
in the single row and modifying two pixels: the original starting position 
of the segment becomes white (0), and the position immediately following 
the original end of the segment becomes the segment's color (if within 
grid bounds). This effectively simulates shifting the segment one position 
to the right.
"""

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
    
    # Iterate to find the first non-white pixel (start of the segment)
    for i, color in enumerate(grid_row):
        if color != 0:
            start_index = i
            segment_color = color
            break
            
    # If no non-white pixel found (all white row), return None for all values
    if start_index == -1:
        return None, None, None
        
    # Find the end of the segment by looking for the last contiguous pixel of the same color
    end_index = start_index
    # Check next pixel as long as it's within bounds and matches the segment color
    while end_index + 1 < len(grid_row) and grid_row[end_index + 1] == segment_color:
        end_index += 1
        
    return start_index, end_index, segment_color

def transform(input_grid):
    """
    Applies the segment shift transformation rule to the input grid.
    
    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed grid.
    """
    # Basic validation for list-of-lists structure
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         # Return an empty structure matching the expected output format if input is invalid
         return [[]] if isinstance(input_grid, list) else [] # Be careful about returning list vs list of lists

    # Handle empty inner list case
    if not input_grid[0]:
        return [[]]

    # Extract the single row and convert to numpy array for efficient processing
    input_row_list = input_grid[0]
    input_row_np = np.array(input_row_list, dtype=int)
    
    # Get grid width
    width = input_row_np.shape[0]
    
    # Initialize the output grid row as a copy of the input row
    output_row_np = np.copy(input_row_np)

    # Find the non-white segment in the input row
    start_index, end_index, segment_color = find_non_white_segment(input_row_np)

    # If a non-white segment was found, apply the transformation modifications
    if start_index is not None:
        # Step 1: Change the pixel at the original start index to white (0)
        # This simulates the segment moving away from this position.
        output_row_np[start_index] = 0
        
        # Step 2: Calculate the target index for the shifted color 
        # This is the position immediately following the segment's original end.
        target_index = end_index + 1
        
        # Step 3: Check if the target index is within the grid bounds
        if target_index < width:
            # Step 4: If within bounds, set the pixel at the target index 
            # in the output row to the segment's original color.
            # This simulates the end of the segment moving into this position.
            output_row_np[target_index] = segment_color
        # Note: If target_index is out of bounds, the color effectively "falls off" the grid,
        # and no action is needed for that specific color placement.

    # Convert the modified numpy row back to a list and wrap it in another list
    # to match the standard ARC grid format (list of lists)
    output_grid = [output_row_np.tolist()]

    return output_grid