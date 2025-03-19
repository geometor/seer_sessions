# 7c008303 • 004 • example_1 • investigate_coder

---
```python
"""
The input grid (9x9) is divided into six non-overlapping rectangular sub-regions.  Top three sub-regions are 3x2, and bottom three are 3x3.
The output grid is created with 6x6 resolution.
For each sub-region in input, select the upper-left pixel.
Map the color of selected input region's upper-left pixel into the same relative position of the output grid, repeating for all regions.
The resulting output grid is 6x6.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid (6x6) with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Define the dimensions of the sub-regions.
    top_region_height = 2
    bottom_region_height = 3
    region_width = 3
    
    # Iterate through the sub-regions and map upper-left pixel color.
    
    # top
    for i in range(2):
        for j in range(3):
            output_grid[i][j*2] = input_grid[i*top_region_height][j * region_width]
            output_grid[i][j*2 + 1] = input_grid[i*top_region_height][j * region_width]

    # bottom
    for i in range(2):
      for j in range(3):
          output_grid[i+2][j*2] = input_grid[i*bottom_region_height+top_region_height*2][j * region_width]
          output_grid[i+2][j*2 + 1] = input_grid[i*bottom_region_height+top_region_height*2][j * region_width]
    

    return output_grid
```
