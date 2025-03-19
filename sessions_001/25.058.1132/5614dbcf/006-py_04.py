"""
1.  **Input:**  Receive an 18x18 grid of colored pixels.
2.  **Region Identification:** Find the single contiguous region of pixels of the same color within the input grid.
3.  **Color Extraction:**  Note the color value of this region.
4. **Output Construction:** Create a 3x3 output grid.
5. **Placement:** Place the extracted color into the top-left cell (0, 0) of the output grid.
6.  **Fill:** Fill the remaining cells of the output grid with black (color value 0).
7.  **Output:** Return the 3x3 output grid.
"""

import numpy as np

def find_region_color(grid):
    """
    Finds the color of the single contiguous region in the grid.
    Assumes there's only one region.
    """
    # Return the color of the first pixel. Since the region is
    # contiguous and of a single color we just need a sample.
    for row in range(grid.shape[0]):
      for col in range(grid.shape[1]):
        color = grid[row,col]
        if color != 0:
          return color

    return 0
   

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the color of the single region
    region_color = find_region_color(input_grid)

    # Place the color in the top-left cell
    output_grid[0, 0] = region_color

    return output_grid