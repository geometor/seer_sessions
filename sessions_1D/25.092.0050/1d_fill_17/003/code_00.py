import copy

"""
Identify the non-white color present in the single row of the input grid. 
Find the indices of the first and second occurrences of this color within that row. 
Create a copy of the input row. Fill the segment of pixels strictly between 
these two indices in the copied row with the identified non-white color. 
Return the modified row within a list to maintain the 2D grid structure.
"""

def find_non_white_pixels(grid_row):
    """
    Finds the color and indices of the two non-white pixels in a 1D grid row.
    
    Args:
        grid_row: A list of integers representing a single row of the grid.

    Returns:
        A tuple (non_white_color, indices) where non_white_color is the integer
        color value (or None if not found correctly) and indices is a sorted 
        list containing the two column indices of the markers (or an empty 
        list if not found correctly).
    """
    non_white_color = None
    indices = []
    
    # First pass to find the non-white color and the first index
    for idx, pixel_color in enumerate(grid_row):
        if pixel_color != 0:
            non_white_color = pixel_color
            indices.append(idx)
            break # Found the first one

    # Check if a non-white color was found
    if non_white_color is None:
        return None, []

    # Second pass to find the second index, starting after the first one
    for idx in range(indices[0] + 1, len(grid_row)):
        pixel_color = grid_row[idx]
        if pixel_color == non_white_color:
            indices.append(idx)
            break # Found the second one

    # Validate that exactly two markers of the *same* color were found
    if len(indices) != 2:
        # This condition handles cases where only one marker is found,
        # or potentially more than two if the logic were different.
        # Based on ARC examples, we expect exactly two.
        # Resetting if the expectation isn't met.
        return None, [] 
        
    # Explicitly check if other non-white colors exist (should not based on examples)
    other_non_white_found = False
    for idx, pixel_color in enumerate(grid_row):
        if pixel_color != 0 and pixel_color != non_white_color:
             other_non_white_found = True
             break
    if other_non_white_found:
         # Invalid input according to observed pattern
         return None, []

    return non_white_color, sorted(indices) # Ensure indices are ordered [start, end]


def transform(input_grid):
    """
    Transforms the input grid by filling the segment between two identical 
    non-white markers in its single row with their color.
    
    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid (1xN).
    """
    
    # Ensure input grid has at least one row
    if not input_grid or not input_grid[0]:
        return copy.deepcopy(input_grid) # Return copy if input is empty or invalid

    # Extract the single row
    input_row = input_grid[0]
    
    # Initialize output_row as a copy of the input row
    # This will be the default return if markers aren't found correctly
    output_row = copy.deepcopy(input_row)

    # Find the marker color and their indices in the row
    marker_color, marker_indices = find_non_white_pixels(input_row)

    # Proceed only if valid markers were found (color is not None and 2 indices)
    if marker_color is not None and len(marker_indices) == 2:
        # Get the start and end column indices for the segment to fill
        # Indices are exclusive of the markers themselves
        start_fill_index = marker_indices[0] + 1
        end_fill_index = marker_indices[1] # range() excludes the end value naturally

        # Fill the segment between the markers in the output row
        for i in range(start_fill_index, end_fill_index):
             # Check index bounds just in case, though logic should prevent out of bounds
             if 0 <= i < len(output_row):
                output_row[i] = marker_color
            
    # Reconstruct the output grid as a list containing the single modified row
    output_grid = [output_row]

    return output_grid