"""
Create an output grid that is twice the height and twice the width of the input grid.
Initialize the output grid with the background color (white, 0).
Copy the input grid into the top-left quadrant of the output grid.
Copy the input grid again into the bottom-right quadrant of the output grid.
The top-right and bottom-left quadrants remain filled with the background color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by tiling it twice into a larger grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the height (H) and width (W) of the input grid.
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # 2. Calculate the dimensions of the output grid.
    output_height = 2 * input_height
    output_width = 2 * input_width

    # 3. Create a new output grid and initialize all cells with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Copy the input grid into the top-left quadrant of the output grid.
    # Rows 0 to input_height-1, columns 0 to input_width-1
    output_grid[0:input_height, 0:input_width] = input_grid

    # 5. Copy the input grid into the bottom-right quadrant of the output grid.
    # Rows input_height to output_height-1, columns input_width to output_width-1
    output_grid[input_height:output_height, input_width:output_width] = input_grid

    # 6. Return the final output grid.
    return output_grid
