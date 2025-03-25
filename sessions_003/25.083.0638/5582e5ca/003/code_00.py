"""
The output is always a 3x3 grid. All cells in the output grid have the same color. This color is one of the colors present in the input grid. The output color appears three times in the input.
"""

import numpy as np

def transform(input_grid):
    # Create a 3x3 output grid, initially filled with zeros (or any default value).
    output_grid = np.full((3, 3), 0)

    # Find the unique colors in the input grid and their counts.
    unique_colors, counts = np.unique(input_grid, return_counts=True)
    
    # Find colors that appear exactly three times.
    target_colors = unique_colors[counts == 3]

    # If the target colors exists - use the first one found, otherwise use default of 0
    if target_colors.size > 0:
      target_color = target_colors[0]
    else:
      target_color = 0
        

    # Fill the output grid with the target color.
    output_grid[:] = target_color

    return output_grid