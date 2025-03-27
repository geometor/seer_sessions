"""
1. Divide Input: Divide the input grid vertically into N equal parts, where N is the ratio of the input height to the output height.
2. Discard: Keep only the top portion.
3. Filter Colors: Keep the colors in the output, discard other colors.
"""

import numpy as np

def transform(input_grid, expected_output):  # Added expected_output back for consistency with previous code
    """Transforms the input grid according to the described rule."""

    input_height = input_grid.shape[0]
    output_height = expected_output.shape[0] # Use expected_output height
    
    if input_height % output_height != 0:
        raise ValueError("Input height must be a multiple of output height.")

    n_parts = input_height // output_height
    top_portion_start = 0
    top_portion_end = input_height // n_parts
    
    output_grid = input_grid[top_portion_start:top_portion_end, :].copy()

    # Get the unique colors present in the expected output.
    allowed_colors = np.unique(expected_output)

    # Create a mask to filter colors not present in the output grid.
    mask = np.isin(output_grid, allowed_colors)
    output_grid[~mask] = 0  # Or some other default, like 0 (white)

    return output_grid