"""
Divides the input grid into 2x1 sections and maps colors based on the presence of maroon (9) and blue (1) pixels.
If maroon is present in the section, the output is red (2). Otherwise, the output is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on 2x1 sections, mapping to red (2) if maroon (9) is present,
    and white (0) otherwise.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height // 2, width), dtype=int)

    # Iterate through each 2x1 section
    for i in range(0, height, 2):
        for j in range(width):
            section = input_grid[i:i+2, j:j+1]

            # Map colors based on section content
            if 9 in section:
                output_grid[i//2, j] = 2  # Red if maroon is present
            else:
                output_grid[i//2, j] = 0  # White otherwise

    return output_grid.tolist()