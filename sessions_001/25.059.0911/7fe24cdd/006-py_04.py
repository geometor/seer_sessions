"""
The transformation rule can be described as follows:

1.  **Expansion:** The input 3x3 grid is expanded into a 6x6 grid.
2.  **Replication:** Each pixel in the input grid is replicated to create a 2x2 block of the same color in the output grid. The position of the 2x2 block corresponds to the position of original pixel within the 3x3 input grid. For example, the pixel at [0, 0] becomes a 2x2 block at the top left corner: [0, 0], [0, 1], [1, 0], [1, 1]. And the pixel at [0, 1] on input will generate a 2x2 block at [0, 2], [0, 3], [1, 2], [1, 3].
"""

import numpy as np

def transform(input_grid):
    # Initialize the 6x6 output grid with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through the input grid.
    for i in range(3):
        for j in range(3):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Create the 2x2 block in the output grid.
            output_grid[2*i:2*i+2, 2*j:2*j+2] = color

    return output_grid