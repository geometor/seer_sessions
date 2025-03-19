"""
1.  **Identify White Regions:** Examine each column of the input grid. Within each column, identify contiguous regions of white pixels (color 0).
2.  **Check for Reflection Condition:** If *all* pixels above the contiguous white region are not white, then perform Step 3.
3.  **Vertical Reflection (Conditional):**
     *   The input is reflected vertically along the axis of a column containing white.
     *   The length of the section that is reflected is the same length above the top of the white region, as the white region itself.
     * The reflected region *replaces* existing pixels
"""

import numpy as np

def get_white_regions(grid):
    """Finds contiguous white regions within each column."""
    white_regions = {}
    for x in range(grid.shape[1]):
      white_indices = np.where(grid[:, x] == 0)[0]
      if len(white_indices) > 0:
        regions = []
        start = white_indices[0]
        for i in range(1, len(white_indices)):
          if white_indices[i] != white_indices[i-1] + 1:
            regions.append((x, start, white_indices[i-1]))
            start = white_indices[i]
        regions.append((x, start, white_indices[-1]))
        white_regions[x] = regions
    return white_regions

def check_reflection_condition(grid, col, white_start):
    """Checks if all pixels above the white region are non-white."""
    if white_start == 0:
      return False  # Nothing above to check
    return np.all(grid[:white_start, col] != 0)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Identify White Regions
    white_regions = get_white_regions(input_grid)
    
    #Vertical Reflection for columns
    for col, regions in white_regions.items():
        for col, white_start, white_end in regions:
          # Check for Reflection Condition
          if check_reflection_condition(input_grid, col, white_start):
              white_height = white_end - white_start + 1
              reflect_height = min(white_start, white_height) #don't reflect beyond grid top

              # Vertical Reflection (Conditional)
              if reflect_height > 0:
                output_grid[white_start - reflect_height:white_start, col] = input_grid[white_start:white_start + reflect_height, col]


    return output_grid