"""
Counts the number of azure (8) pixels along the main diagonal of the input grid and outputs the count as a 1x1 grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by counting azure pixels on the main diagonal.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: A 1x1 grid containing the count of azure pixels on the diagonal.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the size of the grid (assuming it's square).
    grid_size = input_array.shape[0]

    # Initialize a counter for azure pixels on the diagonal.
    azure_count = 0

    # Iterate through the diagonal elements.
    for i in range(grid_size):
        if input_array[i, i] == 8:  # Check if the pixel is azure (8).
            azure_count += 1

    # Create the 1x1 output grid with the count.
    output_grid = [[azure_count]]

    return output_grid