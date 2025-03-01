"""
1.  **Identify:** Locate all azure (8) pixels in the input grid.
2.  **Vertical Propagation:** For each azure pixel in the input, draw a vertical line of azure pixels downwards, taking the original position of each pixel as the x coordinate of the new pixels.
3.  **Horizontal propagation;** From the original y position with an azure pixel, draw a horizontal line using the value of the azure pixels.
"""

import numpy as np

def find_azure_pixels(grid):
    # Find coordinates of all azure (8) pixels
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    azure_pixels = find_azure_pixels(input_grid)
    
    #get the y coordinates for azure pixels
    azure_ys = list(set([y for _, y in azure_pixels]))

    # Vertical Propagation
    for x, y in azure_pixels:
        for i in range(input_grid.shape[0]):
            output_grid[i, x] = 8

    #horizontal propagation
    for y in azure_ys:
      for j in range(input_grid.shape[1]):
          if output_grid[y,j] == 8: #stop drawing when you hit existing line
            break
          output_grid[y,j] = 8

    return output_grid