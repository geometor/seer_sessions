"""
1. Reverse Rows: Reverse the order of the rows in the input grid. The last row becomes the first row, the second-to-last becomes the second, and so on.
2. Sort and Map Colors:
    - In the input, sort the distinct colors present from smallest to largest.
    - In the output, sort the distinct colors present from smallest to largest.
    - Map the smallest input color to the smallest output color, the second smallest to the second smallest, and so on.
"""

import numpy as np

def transform(input_grid):
    # Create a numpy array from the input grid.
    input_np = np.array(input_grid)

    # 1. Reverse the order of rows.
    reversed_rows_np = input_np[::-1]

    # 2. Sort and Map Colors
    # Get unique colors in input and expected output (which are the same)
    input_colors = sorted(np.unique(input_np))

    # Create the color mapping
    color_map = {in_color: in_color for in_color in input_colors}
    
    # Apply the color mapping to the reversed grid
    output_grid = np.vectorize(color_map.get)(reversed_rows_np)

    return output_grid.tolist()