import numpy as np
from typing import List

"""
Expand isolated single colored pixels into 1x3 horizontal blocks.

Iterate through the input row. If a colored pixel (non-zero) is found, check its
horizontal neighbors. If both neighbors are background pixels (0) or out of bounds,
consider this pixel "isolated". Expand the isolated pixel into a 1x3 block of the
same color in the output grid, centered at the original pixel's location. Existing
horizontal blocks of colored pixels (size > 1) and background pixels remain unchanged,
unless overwritten by an expansion.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by expanding isolated colored pixels horizontally.

    Args:
        input_grid: A list of lists representing the input grid (expected to have 1 row).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is treated as a NumPy array for easier handling
    input_np = np.array(input_grid, dtype=int)

    # Check if the input grid is empty or has zero width
    if input_np.shape[0] == 0 or input_np.shape[1] == 0:
        return input_grid # Return original if empty

    # As per the examples, the grid is effectively 1D (a single row)
    # Extract the first (and only) row
    input_row = input_np[0]
    width = len(input_row)

    # Initialize the output row as a copy of the input row
    output_row = input_row.copy()

    # Iterate through each pixel of the input row
    for i in range(width):
        pixel_color = input_row[i]

        # Check if the pixel is colored (not background)
        if pixel_color > 0:
            # Check horizontal neighbors for isolation
            # Check left neighbor (handle boundary)
            left_is_background = (i == 0) or (input_row[i - 1] == 0)
            # Check right neighbor (handle boundary)
            right_is_background = (i == width - 1) or (input_row[i + 1] == 0)

            # If both neighbors are background/boundary, the pixel is isolated
            if left_is_background and right_is_background:
                # Expand the isolated pixel into a 1x3 block in the output_row
                # Set the center pixel (original location)
                output_row[i] = pixel_color
                # Set the left pixel if within bounds
                if i > 0:
                    output_row[i - 1] = pixel_color
                # Set the right pixel if within bounds
                if i < width - 1:
                    output_row[i + 1] = pixel_color

    # Reshape the output row back into the grid format (list of lists)
    output_grid = [output_row.tolist()]
    return output_grid
