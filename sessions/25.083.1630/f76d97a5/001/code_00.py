"""
The task involves transforming an input grid of colors into an output grid.
The primary transformation rule is based on identifying two distinct colors. The spaces where the colors are not present in the original is filled with a neutral color (0).
"""

import numpy as np

def get_colors(grid):
    # get the unique colors
    return np.unique(grid)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    colors = get_colors(output_grid)
    colors_not_0 = [color for color in colors if color != 0]
    
    if len(colors_not_0) != 2:
      color1 = colors_not_0[0]

      for i in range(output_grid.shape[0]):
          for j in range(output_grid.shape[1]):
              # change the border to 0
              if i == 0 or i == output_grid.shape[0] - 1 or j == 0 or j == output_grid.shape[1] - 1:
                  if(output_grid[i][j] == color1):
                      output_grid[i][j] = 0
    else:
      color1 = colors_not_0[0]
      color2 = colors_not_0[1]


      for i in range(output_grid.shape[0]):
          for j in range(output_grid.shape[1]):
              # Check the surroundings of the cell and replace the inner colors with the color 0.
              if i > 0 and i < output_grid.shape[0] - 1 and j > 0 and j < output_grid.shape[1] - 1:
                  if output_grid[i][j] != color1 and output_grid[i][j] != color2:
                    output_grid[i,j] = 0

                  elif not(output_grid[i-1][j] == color1 or output_grid[i-1][j] == color2) or \
                     not(output_grid[i+1][j] == color1 or output_grid[i+1][j] == color2) or \
                     not(output_grid[i][j-1] == color1 or output_grid[i][j-1] == color2) or \
                     not(output_grid[i][j+1] == color1 or output_grid[i][j+1] == color2):
                        output_grid[i][j] = 0

    return output_grid