"""
Reads the value N of the control pixel at (0, 0).
Determines a downward shift amount S based on N using the mapping: {Yellow(4): 3, Magenta(6): 2, Orange(7): 5, Maroon(9): 0}. Defaults to S=0 if N is not in the map.
Creates a new output grid initialized with white (0) of the same dimensions as the input.
Copies the control pixel N to the output grid at (0, 0).
Shifts the content of the input grid from rows 1 downwards by S rows.
Specifically, for each input row r (from 1 to height-1), its content is copied to the output grid at row r + S, if r + S is within the grid's height boundary.
Rows in the output grid from 1 to S remain white (as they were initialized). Content shifted beyond the bottom boundary is lost.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a vertical shift to the grid content (excluding the top-left pixel)
    based on the value of the top-left pixel.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Get the value of the control pixel at (0, 0)
    control_value = input_grid[0, 0]

    # Define the mapping from control pixel value to downward shift amount
    # Based on observed examples: Yellow(4)->3, Magenta(6)->2, Orange(7)->5, Maroon(9)->0
    shift_map = {
        4: 3,
        6: 2,
        7: 5,
        9: 0
    }
    # Determine the shift amount using the map, default to 0 if the value is not found
    shift_amount = shift_map.get(control_value, 0)

    # Place the original control pixel value back into the output grid at (0, 0)
    output_grid[0, 0] = control_value

    # Iterate through the rows of the input grid, starting from the second row (index 1)
    # These are the rows that contain the content to be shifted.
    for r in range(1, height):
        # Calculate the target row index in the output grid after applying the shift
        target_r = r + shift_amount

        # Check if the target row is within the bounds of the grid height
        if target_r < height:
            # If within bounds, copy the entire content of the current input row 'r'
            # to the calculated target row 'target_r' in the output grid.
            # We copy all columns (:) in the row.
            output_grid[target_r, :] = input_grid[r, :]
            # Pixels from input row 'r' that would be shifted beyond the grid height
            # (i.e., if target_r >= height) are effectively discarded, as they are not copied.
            # Rows in the output grid from index 1 up to 'shift_amount' will remain
            # filled with the initial background color (0), as no content is copied there.

    # Return the completed output grid
    return output_grid