"""
1.  **Scan the Input Grid:** Examine the input grid to identify all 2x2 contiguous regions where all four pixels are orange (value 7).
2.  **Select an Orange Region**: If multiple regions are identified, prioritize the region to match the 4x4 output.
3.  **Create Output Grid:** Create a new output grid.
4.  **Map Colors within the 2x2 Region**: For the identified 2x2 orange region in *input* grid:
        Set the corresponding pixel in the *output* grid to green(3).
5. **Map Colors Outside the Region:** For all pixels in the *input* grid that are *not* part of the identified 2x2 orange region. Set the corresponding cells in the output grid to 0.
6. **Return Output Grid**: Return the resulting output grid.
"""

import numpy as np

def find_orange_regions(grid):
    """Finds all 2x2 contiguous regions of orange (7) pixels."""
    orange_regions = []
    for row in range(grid.shape[0] - 1):
        for col in range(grid.shape[1] - 1):
            if np.all(grid[row:row+2, col:col+2] == 7):
                orange_regions.append((row, col))
    return orange_regions

def transform(input_grid):
    """Transforms an input grid to an output grid based on the described rules."""

    orange_regions = find_orange_regions(input_grid)
    output_shape = (4,4)
    output_grid = np.zeros(output_shape, dtype=int)

    if not orange_regions:
      return output_grid

    # use first region found
    row, col = orange_regions[0]

    #create extended region
    extended_region = []
    for r in range(max(0, row - (4-2)) ,min(input_grid.shape[0],row+2)):
        for c in range(max(0,col-(4-2)), min(input_grid.shape[1], col+2)):
            extended_region.append((r,c))

    # Map colors
    for r in range(output_shape[0]):
        for c in range(output_shape[1]):
            input_row = r + row - (output_shape[0] - 2)//2  if row <= input_grid.shape[0]-2 else r
            input_col = c + col - (output_shape[1] - 2)//2  if col <= input_grid.shape[1]-2 else c
            if 0 <= input_row < input_grid.shape[0] and 0<= input_col < input_grid.shape[1]:

              if (input_row, input_col) in extended_region and input_grid[input_row,input_col] == 7 :
                  output_grid[r,c] = 3

    return output_grid