"""
The transformation operates on a grid of pixels. The program iterates through each column of the grid. Within each column, it checks each pixel. If a pixel's color is gray (value 5), it is replaced with a color from a predefined sequence: blue (1), red (2), green (3), and yellow (4). The crucial aspect is that the sequence *restarts* at blue (1) for every new column. Within a single column, the replacement proceeds through the sequence (blue, red, green, yellow), wrapping back to blue if the end of the sequence is reached before the end of the gray pixels in that column. Pixels that are not gray remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Define the color sequence (blue, red, green, yellow)
    color_sequence = [1, 2, 3, 4]

    # Iterate through each column of the grid
    for j in range(cols):
        # Reset the color index to 0 for each new column
        color_index = 0

        # Iterate through each row in the current column
        for i in range(rows):
            # Check if the current pixel is gray (value 5)
            if output_grid[i, j] == 5:
                # Replace the gray pixel with the color at the current color_index
                output_grid[i, j] = color_sequence[color_index % len(color_sequence)]
                # Increment the color index for the next gray pixel in this column
                color_index += 1

    return output_grid