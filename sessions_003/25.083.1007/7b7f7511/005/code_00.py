"""
The transformation rule involves truncating the input grid to match both the height *and* the width of the output grid. The program should determine the target height and width by inspecting the corresponding output grid for each example. No colors are added or removed.
"""

import numpy as np

def transform(input_grid, output_grid):
    """
    Transforms the input grid by truncating it to the dimensions (height and width) of the corresponding output grid.
    """
    # Determine the target dimensions from the provided output grid.
    target_height = len(output_grid)
    target_width = len(output_grid[0])

    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Truncate the input array to the target dimensions.
    output_array = input_array[:target_height, :target_width]

    # Convert the NumPy array back to a list of lists.
    output_grid_transformed = output_array.tolist()

    return output_grid_transformed