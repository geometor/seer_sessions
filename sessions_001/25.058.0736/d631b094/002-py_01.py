"""
1.  **Identify** all pixels with the value '1' (blue) in the input grid.
2.  **Count** the number of identified blue pixels.
3. **Create** the output based on the count. Create a 1xN grid, where N is the number of the blue pixels.
4.  **Fill** all cells of the output grid with the value '1' (blue).
"""

import numpy as np

def transform(input_grid):
    # Find all pixels with value '1' (blue)
    blue_pixels = np.where(input_grid == 1)

    # Count the number of blue pixels
    num_blue_pixels = len(blue_pixels[0])

    # Create an output grid of size 1xN, where N is the number of blue pixels
    output_grid = np.zeros((1, num_blue_pixels), dtype=int)

    # Fill all cells of the output grid with '1' (blue)
    output_grid[:] = 1

    return output_grid