# d6ad076f • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Existing Regions:** Locate the rectangular regions of green (3) at the top and maroon (9) at the bottom of the input grid. Note any all-white (0) area.
2.  **Create Azure Region:** In the center of the grid height of all white (0) rows, insert a rectangular region of azure (8) pixels. The width of this region is 4 pixels.
3.  **Maintain Boundary:** Preserve the exterior outline. All values on the rightmost column remain 0.
4.  **Preserve Regions:** Keep the locations of the green and maroon regions unchanged.
"""

import numpy as np

def find_region(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the white (0) region
    white_region = find_region(input_grid, 0)
    if white_region:
      white_min_row, white_max_row, white_min_col, white_max_col = white_region

      #calculate start and end rows
      start_row = white_min_row
      end_row = white_max_row

      # Calculate the center column for the azure region
      center_col = (white_min_col + white_max_col) // 2

      # Define the width of the azure region (4 pixels)
      azure_width = 4

      # Calculate the start and end columns for the azure region
      azure_start_col = center_col - (azure_width // 2) + 1 # +1 since based on previous center being off by 1
      azure_end_col = center_col + (azure_width // 2)
      
      # Create the azure region
      for row in range(start_row, end_row + 1):  # +1 to be inclusive
          for col in range(azure_start_col, azure_end_col):
            if col < input_grid.shape[1]:
              output_grid[row, col] = 8

    return output_grid
```
