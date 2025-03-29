import numpy as np

"""
Apply a color transformation independently to each column of the input grid.
Create an output grid with the same dimensions as the input grid, initially filled with white (0).
Process each column of the input grid independently, from left to right (column index c from 0 to width-1).
For the current column c:
  a. Initialize a variable current_color to white (0).
  b. Iterate through the rows of this column from bottom to top (row index r from height-1 down to 0).
  c. Read the color of the input pixel at position (r, c), let's call it input_pixel_color.
  d. If input_pixel_color is not white (i.e., not 0), update current_color to be input_pixel_color.
  e. Set the color of the output grid pixel at position (r, c) to the value stored in current_color.
After processing all columns, the resulting output grid is the final result.
"""


def transform(input_grid):
    """
    Transforms the input grid by propagating the lowest non-white color upwards within each column.

    Args:
      input_grid: A list of lists of integers representing the input grid.

    Returns:
      A list of lists of integers representing the transformed output grid.
    """
    # Convert input to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions as the input, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # Iterate through each column independently
    for c in range(width):
        # Initialize the color that will propagate upwards in this column
        current_color = 0  # Start with white (background)

        # Iterate through the rows of the current column from bottom to top
        for r in range(height - 1, -1, -1):
            # Get the color of the pixel in the input grid at (r, c)
            input_pixel_color = input_np[r, c]

            # If the input pixel is not white, update the current propagation color
            # This means the lowest non-white color encountered so far (from the bottom)
            # will become the propagating color.
            if input_pixel_color != 0:
                current_color = input_pixel_color

            # Set the corresponding pixel in the output grid to the current propagation color
            output_grid[r, c] = current_color

    # Convert the numpy array back to a list of lists for the required output format
    return output_grid.tolist()