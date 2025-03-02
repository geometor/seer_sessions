"""
Divides the input grid into 2x1 sections and maps colors based on the presence of maroon (9) and blue (1) pixels.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height // 2, width), dtype=int)

    # Iterate through each 2x1 section
    for i in range(0, height, 2):
        for j in range(width):
            section = input_grid[i:i+2, j:j+1]

            # Map colors based on section content
            if 9 in section:
                output_grid[i//2, j] = 2
            elif 1 in section:
              output_grid[i//2,j] = 0 #explicit null
            else:
                output_grid[i//2, j] = 0

    return output_grid.tolist()