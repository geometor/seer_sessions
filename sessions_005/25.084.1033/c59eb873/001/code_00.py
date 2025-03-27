"""
Scales the input grid by a factor of 2 in both height and width.
Each pixel in the input grid is expanded into a 2x2 square of the same color in the output grid.
The relative positions of these 2x2 blocks in the output correspond to the positions of the original pixels in the input.
"""

import numpy as np

def transform(input_grid):
    """
    Scales the input grid by a factor of 2x2.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the scaled output grid.
    """
    # Convert input grid to a numpy array for easier slicing and dimension access
    input_np = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    input_height, input_width = input_np.shape

    # Calculate the dimensions of the output grid (2*H, 2*W)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (or any placeholder)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color value C of the input pixel at (r, c)
            color = input_np[r, c]

            # Determine the top-left coordinates of the 2x2 block in the output grid
            output_r = r * 2
            output_c = c * 2

            # Fill the 2x2 block in the output grid with the color C
            output_grid[output_r:output_r + 2, output_c:output_c + 2] = color

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
