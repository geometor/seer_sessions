import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into an output grid by scaling it by a factor of 2 
    and replacing pixels based on their color. White input pixels map to a 2x2 
    block of white pixels. Gray input pixels map to a 2x2 block with the pattern 
    [[blue, red], [red, blue]].

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid. 
                                 Contains white(0) and gray(5) pixels.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid. 
                  Contains white(0), blue(1), and red(2) pixels. 
                  Dimensions are twice those of the input grid.
    """

    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid (double the input)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define the replacement pattern for gray pixels
    gray_pattern = np.array([[1, 2], [2, 1]], dtype=int) # [[blue, red], [red, blue]]

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_grid[r, c]

            # Determine the top-left coordinates of the corresponding 2x2 block in the output grid
            output_r_start = r * 2
            output_c_start = c * 2

            # Apply the transformation rules
            if input_color == 5: # If the input pixel is gray(5)
                # Fill the 2x2 block in the output grid with the gray_pattern
                output_grid[output_r_start : output_r_start + 2, output_c_start : output_c_start + 2] = gray_pattern
            # else: # If the input pixel is white(0)
                # The corresponding 2x2 block in the output grid remains white (0), 
                # as it was initialized. No action needed.

    return output_grid