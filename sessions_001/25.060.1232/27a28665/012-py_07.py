"""
The transformation rule involves counting the number of rows that contain at least one azure (8) pixel. The output is a 1x1 grid where the single cell's value is the number of such rows.
"""

import numpy as np

def transform(input_grid):
    """
    Counts the number of rows containing at least one azure (8) pixel.
    Returns the count as a 1x1 grid.
    """
    # Convert the input grid to a NumPy array for easier processing.
    input_grid = np.array(input_grid)

    # Initialize a count of rows with azure pixels.
    row_count = 0

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Check if the color 8 (azure) is present in the current row.
        if 8 in row:
            # Increment the count if azure is found.
            row_count += 1

    # Create a 1x1 output grid with the final count.
    output_grid = np.array([[row_count]])

    return output_grid