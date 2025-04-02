import numpy as np

"""
Iterate through each row of the input grid independently. 
For the current row, identify the non-white color present (C). There will be exactly two pixels with this color.
Find the column index of the leftmost pixel with color C (col_start) and the rightmost pixel with color C (col_end).
Iterate through the columns strictly between col_start and col_end (i.e., from col_start + 1 up to, but not including, col_end).
For each column index c in this range, set the pixel at (current_row, c) in the output grid to color C.
Leave all other pixels unchanged.
"""

def find_marker_indices_and_color(row):
    """
    Finds the column indices and color of the non-white marker pixels in a row.
    Assumes exactly two identical non-white markers per row based on task examples.
    Returns (marker_color, col_start, col_end) or (None, None, None) if assumption fails.
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
            # Determine start and end columns
            col_start = min(col1, col2)
            col_end = max(col1, col2)
            marker_color = color1 # Both colors are the same
            return marker_color, col_start, col_end
            
    # If assumptions (exactly two, identical color) are not met
    return None, None, None

def transform(input_grid):
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
            # Iterate through the column indices strictly *between* the start and end markers
            # range(col_start + 1, col_end) achieves this. If col_end = col_start + 1, the range is empty.
            for c in range(col_start + 1, col_end):
                # Set the color of the pixel at (row r, column c) in the output grid
                # to the identified marker color. This fills the gap.
                output_grid[r, c] = marker_color
                
    # Convert the final numpy array back to a list of lists for the expected ARC format
    return output_grid.tolist()
