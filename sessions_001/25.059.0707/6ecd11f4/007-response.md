# 6ecd11f4 • 007 • refine_coder

---
```python
"""
1. Identify the Target Object: Find a contiguous 3x3 region of pixels, allowing for a single row/column of background color surrounding a solid color. The target region may not be a perfect square. Prioritize regions with uniform color.
2. Extract Subgrid: Extract the 3x3 region.
3. Remove Background: If necessary, remove the background. This may not always be necessary.
"""

import numpy as np

def find_target_region(grid):
    """Finds the 3x3 target region, allowing for surrounding background."""
    rows, cols = grid.shape
    
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = grid[r:r+3, c:c+3]
            unique_colors = np.unique(subgrid)
            
            #if len(unique_colors) <= 2: # Allow background + one other color
            
            # Check if the subgrid is uniform or is mostly one color.
            
            if len(unique_colors) == 1:
                return r, c
            
            # if it is only two colors (a background and a foreground)
            if len(unique_colors) == 2:
                # check if one of the colors forms a solid contiguous block.
                # find counts for each unique color
                counts = [np.sum(subgrid == color) for color in unique_colors]
                # get largest count and index
                largest_count_idx = np.argmax(counts)
                largest_count = counts[largest_count_idx]
                
                # the other_color is the background
                other_color_idx = 1-largest_count_idx
                other_color = unique_colors[other_color_idx]
                
                if largest_count >= 1:
                    return r,c

    return None, None

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify and Extract Target Region
    start_row, start_col = find_target_region(input_grid)
    
    if start_row is None or start_col is None:
        return [[]] # Return empty grid if no target region is found

    output_grid = input_grid[start_row:start_row+3, start_col:start_col+3].copy()

    # 2. No explicit background removal needed, as the target region includes it.

    return output_grid.tolist()
```
