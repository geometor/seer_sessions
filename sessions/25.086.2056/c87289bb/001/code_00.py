"""
Extend vertical azure lines downwards from existing azure pixels until an obstacle (any non-white pixel) or the grid bottom is reached.

1.  Initialize the output grid as an identical copy of the input grid.
2.  Identify the lowermost row in the input grid that contains at least one azure (8) pixel. Let this row index be 'max_r'. If no azure pixels exist, return the copy.
3.  Identify all columns that contain at least one azure (8) pixel at or above row 'max_r'.
4.  For each identified column 'c':
    a.  Starting from the row immediately below 'max_r' (row 'max_r + 1'), scan downwards row by row ('scan_r').
    b.  Check the pixel in the input grid at (scan_r, c).
    c.  If the input pixel is white (0), change the corresponding pixel in the output grid to azure (8).
    d.  If the input pixel is not white (0), stop extending the line in this column 'c'.
    e.  If the scan reaches the bottom of the grid, stop extending the line in this column 'c'.
5.  Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape
    azure_color = 8
    white_color = 0

    # Find the lowermost row containing any azure pixel
    azure_rows = np.where(input_array == azure_color)[0]
    if azure_rows.size == 0:
        # No azure pixels found, return the original grid
        return output_array.tolist()
    max_r = np.max(azure_rows)

    # Identify columns containing azure pixels at or above max_r
    source_columns = set()
    for c in range(width):
        if np.any(input_array[0:max_r+1, c] == azure_color):
            source_columns.add(c)

    # Extend lines downwards for each source column
    for c in source_columns:
        # Start scanning from the row below max_r
        for scan_r in range(max_r + 1, height):
            # Check the color of the pixel in the *original* input grid at the scan position
            if input_array[scan_r, c] == white_color:
                # If it's white, change the corresponding pixel in the output grid to azure
                output_array[scan_r, c] = azure_color
            else:
                # If it's not white (an obstacle), stop extending in this column
                break

    # Convert the NumPy array back to a list of lists for the expected output format
    return output_array.tolist()