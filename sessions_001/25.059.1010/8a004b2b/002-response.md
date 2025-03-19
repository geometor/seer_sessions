# 8a004b2b • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Frame:** Locate the rectangular frame defined by the yellow (color 4) pixels in the corners of the input grid.
2.  **Inner Region:** Determine the dimensions of the inner rectangle enclosed by this yellow frame.
3.  **Create Output Grid:** Create a new, smaller output grid. The height and width of the output grid are the same as the dimensions of the "inner region" divided by 2, rounding down for odd dimensions (integer divison by 2, no remainders).
4. **Merge regions** For each 2 x 2 region inside of the input yellow border, combine into the output grid, into a single cell in the output grid.
5.  **Combine Colors:**
    *    If the cells of the 2x2 region contains only 0 and a single other color, the non-zero color is used.
    *    If a 2x2 region in input contains multiples different colors, the color that is in the bottom right most cell is the output.
"""

import numpy as np

def get_inner_region_bounds(grid):
    # Find coordinates of yellow (4) pixels
    yellow_coords = np.argwhere(grid == 4)
    
    if len(yellow_coords) < 2: # Not enough borders
        return None, None, None, None
    
    # Find top-left and bottom-right yellow pixels
    min_row = min(yellow_coords[:, 0])
    max_row = max(yellow_coords[:, 0])
    min_col = min(yellow_coords[:, 1])
    max_col = max(yellow_coords[:, 1])

    return min_row + 1, max_row, min_col + 1, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    input_grid = np.array(input_grid)  # Ensure numpy array

    # 1. & 2. Identify the Frame and Inner Region
    min_row, max_row, min_col, max_col = get_inner_region_bounds(input_grid)

    if min_row is None:
        return input_grid

    # 3. Create Output Grid
    output_height = (max_row - min_row) // 2
    output_width = (max_col - min_col) // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # 4. & 5. Merge Regions and Combine Colors
    for i in range(output_height):
        for j in range(output_width):
            row_start = min_row + i * 2
            col_start = min_col + j * 2
            region = input_grid[row_start:row_start+2, col_start:col_start+2]

            # Get unique non-zero colors
            unique_colors = np.unique(region[region != 0])

            if len(unique_colors) == 1:
                output_grid[i, j] = unique_colors[0]  # Single non-zero color
            elif len(unique_colors) > 1:
                output_grid[i,j] = region[1,1] # use the bottom right pixel value
            else:
                output_grid[i,j] = 0

    return output_grid
```
