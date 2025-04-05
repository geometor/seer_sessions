import numpy as np

"""
Transforms an input grid into an output grid of the same dimensions by tiling a 2x2 pattern extracted from the top-left corner of the input grid.
The value of each cell in the output grid at position (r, c) is determined by the value in the input grid at position (r % 2, c % 2).
"""

def transform(input_grid):
    """
    Applies a tiling transformation based on the top-left 2x2 pattern of the input grid.

    Args:
        input_grid (list of list of int): The input grid represented as a list of lists.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to a numpy array for easier indexing and dimension handling
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_array.shape

    # Initialize an output grid (numpy array) with the same dimensions, filled with zeros initially
    output_array = np.zeros((height, width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(height):
        for c in range(width):
            # Calculate the source row index using modulo 2
            source_r = r % 2
            # Calculate the source column index using modulo 2
            source_c = c % 2
            # Assign the value from the corresponding top-left 2x2 cell of the input grid
            output_array[r, c] = input_array[source_r, source_c]

    # Convert the output numpy array back to a list of lists for the final return format
    output_grid = output_array.tolist()

    return output_grid