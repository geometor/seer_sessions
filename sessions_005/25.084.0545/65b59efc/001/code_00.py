"""
1.  Transpose the input grid.
2.  Identify the non-zero colors in the last row of the transposed input grid. Create a color map using the index as the key and color as value.
3.  Iterate through the transposed *output* grid.
4.  Within the output grid, the colors in the input grid are shifted using a cyclic shift by a factor equal to index of the color in the last row of unique colors.
"""

import numpy as np

def transpose(grid):
    return np.transpose(grid)

def create_color_map(row):
    color_map = {}
    j=0
    for i, color in enumerate(row):
      if color!=0:
        color_map[j] = color
        j+=1

    return color_map

def transform(input_grid):
    # Transpose the input grid
    transposed_grid = transpose(input_grid)

    # Create a color map from the last row of the original (untransposed) grid
    color_map = create_color_map(input_grid[-1])

    # Initialize the output grid with the shape of transposed grid.
    output_grid = np.zeros_like(transposed_grid)
    rows, cols = transposed_grid.shape
    
    # Iterate and transform
    for r in range(rows):
        for c in range(cols):
          #shift all non zero colors
          pixel = transposed_grid[r,c]
          if pixel !=0:
            for i, val in enumerate(color_map.values()):
              if pixel==val:
                output_grid[r,c] = color_map.get((i + 1) % len(color_map),0)
          #except 0
          else:
            output_grid[r,c] = transposed_grid[r,c]
            

    return output_grid