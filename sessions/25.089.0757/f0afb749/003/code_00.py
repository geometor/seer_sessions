import numpy as np

"""
Transforms an input grid into an output grid based on pixel color by scaling the grid by 2x.

The output grid is twice the height and twice the width of the input grid.
Each pixel in the input grid maps deterministically to a 2x2 block of pixels in the output grid.

Transformation Rule:
1. Determine the dimensions of the input grid (height H, width W).
2. Create an output grid with dimensions (H*2, W*2), initialized typically with white (0).
3. Iterate through each pixel (r, c) in the input grid.
4. Get the color 'C' of the input pixel input_grid[r, c].
5. Determine the corresponding 2x2 block in the output grid, which starts at row r*2 and column c*2.
6. Apply the specific mapping based on the input pixel's color 'C':
   - If the input pixel color 'C' is white (0), the corresponding 2x2 output block becomes:
     [[1, 0],  # Top-left: blue, Top-right: white
      [0, 1]]  # Bottom-left: white, Bottom-right: blue
     This forms a diagonal pattern of blue pixels.
   - If the input pixel color 'C' is non-white (any color from 1 to 9), the corresponding 2x2 output block is filled entirely with that color 'C':
     [[C, C],
      [C, C]]
7. Populate the output grid according to these rules for all input pixels.
8. Return the completed output grid.
"""

def transform(input_grid):
    """
    Applies the scaling and color transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier handling and shape access
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions (double the input dimensions)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (white)
    # Using zeros is convenient as white is one of the fill colors
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
                # Fill the 2x2 block with the blue diagonal pattern
                output_grid[output_r_start, output_c_start] = 1      # Top-left -> blue
                output_grid[output_r_start, output_c_start + 1] = 0  # Top-right -> white (already 0, explicit for clarity)
                output_grid[output_r_start + 1, output_c_start] = 0  # Bottom-left -> white (already 0, explicit for clarity)
                output_grid[output_r_start + 1, output_c_start + 1] = 1  # Bottom-right -> blue
            else:  # Non-white pixel case
                # Fill the 2x2 block entirely with the input color
                output_grid[output_r_start:output_r_start+2, output_c_start:output_c_start+2] = input_color
                # # Equivalent explicit assignment:
                # output_grid[output_r_start, output_c_start] = input_color     # Top-left
                # output_grid[output_r_start, output_c_start + 1] = input_color # Top-right
                # output_grid[output_r_start + 1, output_c_start] = input_color # Bottom-left
                # output_grid[output_r_start + 1, output_c_start + 1] = input_color # Bottom-right

    return output_grid