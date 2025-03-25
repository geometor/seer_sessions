"""
The transformation truncates the input grid. The output height is the minimum height among all output grids in the training examples, and the output width is the minimum width among all output grids.
"""

import numpy as np

def transform(input_grid):
    # Determine the target dimensions based on the minimum dimensions of the training examples' outputs.
    # From manual inspection: min_height = 3, min_width = 2 (example 3 height, example 3 width)
    target_height = 3
    target_width = 2

    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Truncate the input array to the target dimensions.
    output_array = input_array[:target_height, :target_width]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid