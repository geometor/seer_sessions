import numpy as np

"""
Iterate through each row of the input grid independently. For each row, find the pair of identical non-white pixels. Determine the leftmost (col_start) and rightmost (col_end) column indices of these pixels. Fill all pixels in the row from col_start to col_end (inclusive) with the color of the marker pixels. Leave all other pixels unchanged.
"""

def find_marker_indices_and_color(row):
    """
    Finds the column indices and color of the non-white marker pixels in a row.
    Assumes exactly two identical non-white markers per row based on task examples.
    Returns (marker_color, col_start, col_end) or (None, None, None) if assumption fails.
    
    Args:
        row (np.array): A single row from the input grid.

    Returns:
        tuple: (marker_color, col_start, col_end) if valid markers found, 
               (None, None, None) otherwise. marker_color is the integer color value,
               col_start is the minimum column index, col_end is the maximum column index.
    """
    # Find indices of all non-zero (non-white) elements
    indices = np.where(row != 0)[0] 
    
    # Check if exactly two non-white pixels are found
    if len(indices) == 2:
        # Get the column indices
        col1, col2 = indices[0], indices[1]
        # Get the colors at these indices
        color1 = row[col1]
        color2 = row[col2]
        
        # Check if the colors are the same
        if color1 == color2:
            # Determine start and end columns (minimum and maximum index)
            col_start = min(col1, col2)
            col_end = max(col1, col2)
            marker_color = color1 # Both colors are the same
            return marker_color, col_start, col_end
            
    # If assumptions (exactly two, identical color) are not met
    return None, None, None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    For each row, it finds the pair of identical non-white pixels and fills 
    the horizontal segment between and including them with their color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify and return as the output
    # This ensures the original input is not changed and pixels outside the
    # transformation range retain their original values.
    output_grid = np.copy(input_np)
    
    # Get the number of rows in the grid
    height = input_np.shape[0]

    # Iterate through each row index
    for r in range(height):
        # Get the current row from the input grid
        current_row = input_np[r]
        
        # Find the marker color and the start/end columns for this row
        marker_color, col_start, col_end = find_marker_indices_and_color(current_row)

        # Check if valid markers were found in the row
        if marker_color is not None:
            # Iterate through the column indices *including* the start and end markers
            # range(col_start, col_end + 1) achieves this inclusive range.
            for c in range(col_start, col_end + 1):
                # Set the color of the pixel at (row r, column c) in the output grid
                # to the identified marker color. This fills the horizontal segment.
                output_grid[r, c] = marker_color
                
    # Convert the final numpy array back to a list of lists for the expected ARC format
    return output_grid.tolist()
