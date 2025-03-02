"""
1.  **Identify Red Regions**: Examine the input grid and identify contiguous regions of red pixels. Each of these regions is treated as a single object.
2.  **Determine the shape**: Find the shape of the red pixel region.
3.  **Replicate with Gray**: Create an output grid where the shape is replicated using gray pixels in place of the red ones. The position and overall shape of the red region in the input directly correspond to the position and shape of the gray region in the output.
4. **Output Size**: The size of the gray area depends on the input size of red area.
"""

import numpy as np

def find_red_regions(grid):
    """
    Finds contiguous regions of red pixels in the input grid.
    Returns a list of coordinates of red pixels.
    """
    red_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:  # Red pixel
                red_pixels.append((i, j))
    return red_pixels

def transform(input_grid):
    input_grid = np.array(input_grid)
    
    # Find the coordinates of all red pixels
    red_regions = find_red_regions(input_grid)
    
    # If no red pixels are found, return an empty grid or a default grid
    if not red_regions:
        return np.zeros_like(input_grid).tolist()

    # Determine the shape of the red regions
    max_row = max(r[0] for r in red_regions)
    min_row = min(r[0] for r in red_regions)
    max_col = max(r[1] for r in red_regions)
    min_col = min(r[1] for r in red_regions)

    # output grid with the shape of input
    output_grid = np.zeros_like(input_grid)
    
    
    # Replicate the red shape with gray pixels
    for row, col in red_regions:
      output_grid[row,col] = 5

    return output_grid.tolist()