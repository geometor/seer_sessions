"""
1. **Identify Target Color:** Determine the single non-zero color (the "target color") present in the input grid. If there is no non-zero color return an empty grid.

2. **Count Target Color Occurrences:**
   - Count the number of times the target color appears in the first row (top_count).
   - Count the number of times the target color appears in the first column (side_count).

3. **Determine Output Grid Dimensions:**
    - If both `top_count` and `side_count` are 0, the output is an empty array.
    - if `top_count` is zero, and side_count is not zero, the output grid is 1 x (side_count * (top_count + 1))
    - If `side_count` is zero, and top_count is not zero, the output grid is 1 x top_count.
    - If neither `top_count` nor `side_count` is zero, the output grid is 1 x ((top_count + 1) * side_count).

4. **Create and Populate Output Grid:** Create a new grid with the calculated dimensions (height x width) and fill every cell of this grid with the target color.

5.  **Return output grid** Return the resulting grid.
"""

import numpy as np

def get_target_color(grid):
    # Find the unique non-zero color in the grid
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return 0

def count_top_side(grid, target_color):
    # Count target color along top and side
    top_count = 0
    for x in grid[0]:
        if x == target_color:
            top_count+=1
    
    side_count = 0
    for row in grid:
       if row[0] == target_color:
           side_count += 1
    return top_count, side_count

def transform(input_grid):
    # initialize output_grid

    # Find the target (non-zero) color
    target_color = get_target_color(input_grid)

    if target_color == 0:
        return np.array([])
       
    top_count, side_count = count_top_side(input_grid, target_color)
    
    # Determine output dimensions
    if top_count == 0 and side_count == 0:
        width = 0
        height = 0
    elif top_count == 0:
        width = side_count * (top_count + 1)
        height = 1
    elif side_count == 0:
        width = top_count
        height = 1
    else:
        width = (top_count + 1) * side_count
        height = 1
        
    # Construct the output grid and fill with the target color
    output_grid = np.full((height, width), target_color)


    return output_grid