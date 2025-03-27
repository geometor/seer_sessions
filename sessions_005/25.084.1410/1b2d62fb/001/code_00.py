"""
Compares two 5x3 subgrids within a 5x7 input grid, separated by a vertical blue line in column 3.
Creates a 5x3 output grid. An output pixel is set to azure (8) if the corresponding pixels in both input subgrids are identical and white (0). Otherwise, the output pixel is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on pixel comparison across a central divider.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """

    # Get input grid dimensions
    height, width = input_grid.shape

    # Define the width of the subgrids and the divider column index
    # Assuming the structure observed in examples: 7 columns total, divider at index 3
    subgrid_width = 3
    divider_col = 3
    
    # Check if input dimensions match expected format (optional but good practice)
    if width != 2 * subgrid_width + 1 or divider_col != subgrid_width:
        print(f"Warning: Input grid dimensions ({height}x{width}) or divider position might not match expected format (Hx{2*subgrid_width+1} with divider at {subgrid_width}).")
        # Attempt to proceed anyway based on the assumption

    # Initialize the output grid with the background color (white, 0)
    # Output grid has the same height as input and the width of a subgrid
    output_grid = np.zeros((height, subgrid_width), dtype=int)

    # Iterate through each cell position of the subgrids
    for r in range(height):
        for c in range(subgrid_width):
            # Get pixel value from the left subgrid
            left_pixel = input_grid[r, c]

            # Get pixel value from the corresponding position in the right subgrid
            # The right subgrid starts after the divider column
            right_pixel_col = c + divider_col + 1
            # Ensure the column index is within bounds (safety check)
            if right_pixel_col < width:
                right_pixel = input_grid[r, right_pixel_col]
            else:
                # Handle cases where the right column might be out of bounds
                # based on unexpected input dimensions. Setting to a value
                # that won't satisfy the condition (e.g., -1) or skipping.
                # Here, we'll just skip the comparison for this cell.
                continue 

            # Check the condition: both pixels are equal AND they are white (0)
            if left_pixel == right_pixel and left_pixel == 0:
                # Set the corresponding output pixel to azure (8)
                output_grid[r, c] = 8
            # Otherwise, the output pixel remains white (0) as initialized

    return output_grid