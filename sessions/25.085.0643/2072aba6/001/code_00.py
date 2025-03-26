"""
Transforms an input grid into an output grid that is double the size.
Each pixel in the input grid maps to a 2x2 block in the output grid.
- If the input pixel is white (0), the corresponding 2x2 block in the output grid is filled with white (0).
- If the input pixel is gray (5), the corresponding 2x2 block in the output grid is filled with the pattern [[blue, red], [red, blue]] (i.e., [[1, 2], [2, 1]]).
The position of the 2x2 block in the output grid is determined by multiplying the row and column indices of the input pixel by 2.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define the pattern for gray input pixels
    gray_pattern = np.array([[1, 2], [2, 1]], dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_np[r, c]

            # Determine the top-left corner of the 2x2 block in the output grid
            output_r = r * 2
            output_c = c * 2

            # Apply the transformation rule based on the input color
            if input_color == 5:  # Gray
                # Place the gray pattern in the corresponding 2x2 block
                output_grid[output_r:output_r + 2, output_c:output_c + 2] = gray_pattern
            # elif input_color == 0: # White
                # The block is already initialized to white (0), so no action needed

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
