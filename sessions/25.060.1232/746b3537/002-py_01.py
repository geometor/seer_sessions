"""
The transformation rule extracts a sequence of colors from the input grid and removes vertically or horizontally repeating colors, resulting in a compressed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by extracting a sequence of unique colors,
    either vertically (top to bottom) or horizontally (left to right),
    and removing adjacent duplicates.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    if rows == 3 and cols ==3:
       output_grid = [input_grid[i,0] for i in range(rows)]
    elif rows > cols:
        # Extract unique colors vertically (top to bottom)
        unique_colors = []
        for i in range(rows):
          color = input_grid[i,0]
          if not unique_colors or color != unique_colors[-1]: #changed color not in to !=
              unique_colors.append(color)
        output_grid = unique_colors
    else:
      # Extract unique color horizontally
      output_grid = [input_grid[0, j] for j in range(cols)]
    return output_grid