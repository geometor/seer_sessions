"""
Divides the input grid into 2x1 vertical sections and maps the output pixel value to the top pixel's value of each section.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on 2x1 sections, mapping the output to the top value of each section.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height // 2, width), dtype=int)

    # Iterate through each 2x1 section
    for i in range(0, height, 2):
        for j in range(width):
            # Get the top value of the section
            top_value = input_grid[i, j]

            # Map the top value to the output grid
            output_grid[i//2, j] = top_value

    return output_grid.tolist()