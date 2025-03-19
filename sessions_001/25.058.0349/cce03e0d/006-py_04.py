"""
The transformation rule appears to selectively expand only '0' (white) pixels that are surrounded by '8' (azure) pixels. The expansion is not a full plus shape; it seems to only extend in the direction of the azure pixels. If a '0' pixel is only surrounded by azure on specific sides, it only expands those directions.

Revised Natural Language Program:

1.  **Identify Target Pixels:** Find all '0' (white) pixels in the input grid.
2.  **Check Surroundings:** For each '0' pixel, check its immediate neighbors (up, down, left, right).
3.  **Conditional Expansion:** If a neighbor is an '8' (azure) pixel, then, in the output grid, set the corresponding neighbor of the *expanded* '0' pixel to '0' as well. The center of the 0 pixel's location is also set to 0.
4. Other white pixels, and all other color pixels, are ignored. The output should preserve the background of azure.

"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule: expanding '0' pixels surrounded by '8' pixels.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3

    # Initialize output_grid with '8' (azure) - background color
    output_grid = np.full((output_height, output_width), 8, dtype=int)

    # Iterate through the input grid and find '0' pixels
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 0:
                # Calculate the corresponding center position in the output grid
                output_row = row * 3 + 1
                output_col = col * 3 + 1

                # Set the center pixel to '0'
                output_grid[output_row, output_col] = 0

                # Check neighbors and expand conditionally
                if row > 0 and input_grid[row - 1, col] == 8:  # Top
                    output_grid[output_row - 1, output_col] = 0
                if row < input_height - 1 and input_grid[row + 1, col] == 8:  # Bottom
                    output_grid[output_row + 1, output_col] = 0
                if col > 0 and input_grid[row, col - 1] == 8:  # Left
                    output_grid[output_row, output_col - 1] = 0
                if col < input_width - 1 and input_grid[row, col + 1] == 8:  # Right
                    output_grid[output_row, output_col + 1] = 0

    return output_grid