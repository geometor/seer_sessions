"""
Transforms a 1D sequence of pixels based on value and position.

Iterates through the input sequence.
If a pixel is white (0), it remains white (0) in the output.
If a pixel is blue (1):
  - If its index is between 2 and 7 (inclusive), it becomes azure (8) in the output.
  - Otherwise (index < 2 or index > 7), it becomes gray (5) in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list of integers representing the input pixel sequence.

    Returns:
        A list of integers representing the transformed output pixel sequence.
    """
    # Initialize output_grid as a list of the same size as input_grid
    output_grid = [0] * len(input_grid)

    # Iterate through the input sequence with index and value
    for i, pixel_value in enumerate(input_grid):
        # Check if the pixel is white (0)
        if pixel_value == 0:
            # Keep white pixels as white
            output_grid[i] = 0
        # Check if the pixel is blue (1)
        elif pixel_value == 1:
            # Check the index condition
            if 2 <= i <= 7:
                # Change blue to azure (8) if index is between 2 and 7
                output_grid[i] = 8
            else:
                # Change blue to gray (5) otherwise
                output_grid[i] = 5
        # Handle potential unexpected input values (optional, but good practice)
        # else:
        #    output_grid[i] = pixel_value # or raise an error, or map to a default

    return output_grid