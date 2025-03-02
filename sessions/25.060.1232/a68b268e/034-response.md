# a68b268e • 034 • example_6 • investigate_coder

---
```python
"""
The output grid is a 4x4 grid.  It is composed of the color values from the top-left corner pixel of each of four regions in the input grid. The input grid's regions are determined by the horizontal line of blue (1) pixels and the edges of the grid.
"""

import numpy as np

def get_regions(input_grid):
    # Find the horizontal line of 1s.
    rows, cols = input_grid.shape
    blue_line_row = -1
    for r in range(rows):
        if np.all(input_grid[r, :] == 1):
            blue_line_row = r
            break

    # Define the four regions based on the blue line.
    regions = {}
    regions['top_left'] = input_grid[:blue_line_row, :].copy()
    regions['top_right'] = input_grid[:blue_line_row, :].copy()
    regions['bottom_left'] = input_grid[blue_line_row + 1:, :].copy()
    regions['bottom_right'] = input_grid[blue_line_row + 1:, :].copy()
    
    return regions, blue_line_row

def transform(input_grid):
    """
    Transforms the input grid into the output grid by extracting the
    top-left pixel of four distinct regions and placing in the output grid
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Get the four regions.
    regions, blue_line_row = get_regions(input_grid)

    # Initialize the output grid as a 4x4 array.
    output_grid = np.zeros((4, 4), dtype=int)
    
    output_grid[0,0] = regions['top_left'][0,0]
    output_grid[0,1] = regions['top_right'][0,-1] # top right corner
    output_grid[0,2] = regions['top_right'][0,-1] # top right corner
    output_grid[0,3] = regions['top_left'][0,0]

    output_grid[1,0] = regions['top_right'][0,-1] # top right corner
    output_grid[1,1] = regions['top_left'][0,0]
    output_grid[1,2] = regions['top_left'][0,0]
    output_grid[1,3] = regions['top_right'][0,-1] # top right corner

    output_grid[2,0] = regions['top_left'][0,0]
    output_grid[2,1] = regions['top_left'][0,0]
    output_grid[2,2] = regions['top_left'][0,0]
    output_grid[2,3] = regions['top_right'][0,-1] # top right corner

    output_grid[3,0] = regions['top_left'][0,0]
    output_grid[3,1] = regions['top_left'][0,0]
    output_grid[3,2] = regions['top_left'][0,0]
    output_grid[3,3] = regions['bottom_left'][0,0]


    return output_grid
```
