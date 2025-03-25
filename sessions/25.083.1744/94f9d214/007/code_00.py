"""
1. **Identify the Blue Region:** Find the smallest rectangular region within the input grid that contains all the blue (1) pixels.
2. **Flip the Blue Region:** Flip this region both vertically (up/down) and horizontally (left/right).
3. **Create Output Grid:** Initialize a 4x4 output grid filled with white (0).
4. **Place Flipped Region:** Place the flipped blue region onto the top-left corner of a temporary grid that has the same dimensions as the input grid.
5. **Replace and Crop:** In the temporary grid, replace all blue (1) pixels with red (2) pixels.  Then, extract the top-left 4x4 portion of this temporary grid to create the final output grid.
"""

import numpy as np

def get_blue_region(input_grid):
    """Extracts the subgrid containing only the blue (1) pixels."""
    rows, cols = np.where(input_grid == 1)
    if len(rows) == 0:
        return np.array([])
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return input_grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Identify the blue region
    blue_region = get_blue_region(input_grid)

    # Initialize output_grid as 4x4 filled with 0
    output_grid = np.zeros((4, 4), dtype=int)
    
    if blue_region.size == 0:
        return output_grid

    # Flip the blue region both vertically and horizontally
    flipped_region = blue_region[::-1, ::-1]

    # Create a temporary grid with same dimensions as input
    temp_grid = np.zeros_like(input_grid)

    # Place the flipped region onto the top-left corner of temporary grid
    rows, cols = flipped_region.shape
    temp_grid[:rows, :cols] = flipped_region
    
    # Replace 1s with 2s in the temporary grid
    temp_grid = np.where(temp_grid == 1, 2, temp_grid)

    # Extract the top-left 4x4 portion of the temporary grid
    output_grid = temp_grid[:4, :4]

    return output_grid