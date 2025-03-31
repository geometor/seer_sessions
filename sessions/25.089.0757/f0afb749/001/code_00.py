import numpy as np

"""
Transforms an input grid into an output grid based on pixel color.

The output grid is twice the height and twice the width of the input grid.
Each pixel in the input grid maps to a 2x2 block in the output grid.

Transformation Rule:
- If an input pixel is white (0), its corresponding 2x2 output block becomes:
  [[1, 0],
   [0, 1]] (blue diagonal, white off-diagonal).
- If an input pixel is non-white (color C), its corresponding 2x2 output block
  is filled entirely with color C:
  [[C, C],
   [C, C]].
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid (e.g., with zeros)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_np[r, c]

            # Calculate the top-left coordinates of the 2x2 output block
            output_r_start = r * 2
            output_c_start = c * 2

            # Apply the transformation rule based on the input color
            if input_color == 0:  # White pixel case
                output_grid[output_r_start, output_c_start] = 1  # Top-left -> blue
                output_grid[output_r_start, output_c_start + 1] = 0  # Top-right -> white
                output_grid[output_r_start + 1, output_c_start] = 0  # Bottom-left -> white
                output_grid[output_r_start + 1, output_c_start + 1] = 1  # Bottom-right -> blue
            else:  # Non-white pixel case
                output_grid[output_r_start, output_c_start] = input_color     # Top-left
                output_grid[output_r_start, output_c_start + 1] = input_color # Top-right
                output_grid[output_r_start + 1, output_c_start] = input_color # Bottom-left
                output_grid[output_r_start + 1, output_c_start + 1] = input_color # Bottom-right

    return output_grid