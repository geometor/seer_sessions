import numpy as np

"""
Create an output grid based on an input grid. The output grid has the same width 
as the input grid but half the height. A pixel in the output grid is set to red (2) 
if and only if the corresponding pixel in the top half of the input grid AND the 
corresponding pixel in the bottom half of the input grid are both white (0). 
Otherwise, the output pixel is white (0).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the rule:
    Output pixel (r, c) is red (2) if input pixels (r, c) and (r + H/2, c) are both white (0).
    Otherwise, output pixel (r, c) is white (0).

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the height of the output grid (which is also the height of the top/bottom halves)
    output_height = input_height // 2
    output_width = input_width

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel coordinate of the output grid (and the top half of the input)
    for r in range(output_height):
        for c in range(output_width):
            # Get the color of the pixel in the top half of the input grid
            top_pixel_color = input_grid[r, c]

            # Get the color of the corresponding pixel in the bottom half of the input grid
            # The row index in the input grid is r + output_height
            bottom_pixel_color = input_grid[r + output_height, c]

            # Check if both corresponding pixels in the input grid are white (0)
            if top_pixel_color == 0 and bottom_pixel_color == 0:
                # If both are white, set the output pixel to red (2)
                output_grid[r, c] = 2
            # Otherwise, the output pixel remains white (0) as initialized

    return output_grid
