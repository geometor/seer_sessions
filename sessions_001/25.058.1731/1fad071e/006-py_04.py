"""
1. Identify Unique Colors: Examine the *entire* input grid and identify all unique color values present, preserving the order of their first appearance.
2. Determine Output Dimensions: Create a 1 x N output grid, where N is the number of unique colors found in the input grid.
3. Populate Output: Fill the output grid with the ordered sequence of unique colors.
"""

import numpy as np

def transform(input_grid):
    # Find unique colors in order of appearance in the entire grid.
    unique_colors = []
    for row in input_grid:
        for color in row:
            if color not in unique_colors:
                unique_colors.append(color)

    # Determine the output grid dimensions (1 x N, where N is the number of unique colors).
    num_unique_colors = len(unique_colors)
    output_grid = np.zeros((1, num_unique_colors), dtype=int)

    # Populate the output grid with the unique colors.
    for i in range(num_unique_colors):
        output_grid[0, i] = unique_colors[i]

    return output_grid