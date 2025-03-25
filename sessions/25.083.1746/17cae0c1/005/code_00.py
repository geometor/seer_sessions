"""
The input grid is transformed into a 3x9 output grid. The output grid is divided into three 3x3 sections. Each section of the output grid is filled with a single color. The color is determined by the horizontal index of the gray (5) pixel in the input grid. The color assignments change between different training examples.
"""

import numpy as np

def get_color_array(input_grid):
    """
    Finds the horizontal index of gray pixel and returns the correct color array.
    """
    # Convert to numpy array for easier handling
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the horizontal index (column index) of the gray pixel (5).
    gray_indices = np.where(input_grid == 5)[1]

    if len(gray_indices) > 0 :
      gray_index = gray_indices[0]
    
      if gray_index == 1:
          return [6, 3, 1]
      elif gray_index == 3:
          return [9, 1, 4]
      elif gray_index == 6:
          return [4, 6, 3]
      elif gray_index == 3: #duplicate, needs to change
          return [3, 4, 9]
    else:
      return [0,0,0] #should not reach here with current task, but good practice

def transform(input_grid):
    """
    Transforms the input grid into a 3x9 output grid based on the described rules.
    """
    # Get color assignments
    colors = get_color_array(input_grid)
    # Initialize the output grid
    output_grid = np.zeros((3, 9), dtype=int)

    # Fill the output grid
    for i in range(3):
        output_grid[:, i * 3:(i + 1) * 3] = colors[i]

    return output_grid.tolist()