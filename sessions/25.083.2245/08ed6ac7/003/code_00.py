"""
The transformation rule operates on a grid of pixels. Each pixel with the color gray (value 5) is replaced by a color from a predefined sequence: blue, red, green, and yellow. This sequence is applied cyclically. Critically, the sequence restarts at the beginning (blue) for each new *column* that contains gray pixels. The color assignment within a single column proceeds through the sequence (blue, then red, then green, then yellow), wrapping back to blue if necessary. Non-gray pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create a color sequence to replace gray pixels
    color_sequence = [1, 2, 3, 4]  # Blue, Red, Green, Yellow

    # Iterate through each column
    for j in range(cols):
        # Reset color index for each column
        color_index = 0
        # Iterate through each cell in the column
        for i in range(rows):
            # Check if the pixel is gray
            if output_grid[i, j] == 5:
                # Replace the gray pixel with the current color in the sequence
                output_grid[i, j] = color_sequence[color_index % len(color_sequence)]
                # Move to the next color in the sequence
                color_index += 1

    return output_grid