import numpy as np

"""
Identifies the non-white color (C) present in the input row.
Finds the first (min_index) and last (max_index) occurrences of this color C.
Fills the segment of the row between min_index and max_index (inclusive) with color C.
Pixels outside this segment remain white (0).
"""

def find_non_white_pixels(grid):
    """Finds the color and indices of non-white pixels."""
    non_white_color = -1
    indices = []
    for index, pixel in enumerate(grid):
        if pixel != 0:
            if non_white_color == -1:
                non_white_color = pixel
            # Ensure we only consider the target non-white color
            if pixel == non_white_color:
                indices.append(index)
    return non_white_color, indices

def transform(input_grid):
    """
    Fills the segment between two non-white pixels of the same color
    in a 1D input grid.

    Args:
        input_grid: A list or 1D numpy array representing the input row.

    Returns:
        A list representing the transformed output row.
    """
    # Convert to numpy array for easier handling if it's a list
    # Note: ARC tasks usually provide numpy arrays, but handle lists too
    if isinstance(input_grid, list):
        input_grid = np.array(input_grid)
        
    # Assuming the input is always 1D as per examples
    if input_grid.ndim > 1:
        # Handle potential nested list/array for single row case
        if input_grid.shape[0] == 1:
             input_row = input_grid[0]
        else:
             raise ValueError("Input grid must be 1-dimensional or a single row.")
    else:
         input_row = input_grid
         
    # Initialize output_grid as a copy of the input row
    output_row = list(input_row) # Work with a list copy

    # Find the non-white color and its indices
    non_white_color, indices = find_non_white_pixels(output_row)

    # Check if exactly two non-white pixels of the same color were found
    if non_white_color != -1 and len(indices) >= 2:
        # Find the minimum and maximum indices
        start_index = min(indices)
        end_index = max(indices)

        # Fill the segment between start_index and end_index (inclusive)
        for i in range(start_index, end_index + 1):
            output_row[i] = non_white_color
            
    # If input was originally a numpy array, convert back if needed,
    # but standard ARC evaluation expects list of lists or numpy array.
    # Returning a list is generally safe.
    # If the original input was shaped (1, N), return [[...]]
    if input_grid.ndim > 1 and input_grid.shape[0] == 1:
        return [output_row]
    else:
        return output_row # Return as a flat list if input was 1D