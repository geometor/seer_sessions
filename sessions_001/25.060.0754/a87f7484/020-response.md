# a87f7484 • 020 • refine_coder

---
```python
"""
1.  **Identify 3x3 Sub-grids:** Examine the input grid to find all possible 3x3 sub-grids.
2.  **Find Solid Color Regions:** Find all 3x3 regions composed of a single, non-zero color.
3.  **Construct Output:** If such a region exists, the output grid is an exact copy of one of these 3x3 sub-grids. If multiple such regions exist, use the one that is first encountered when scanning from top-to-bottom and left-to-right. If no such region exists, return an empty grid.
"""

import numpy as np

def find_solid_color_subgrids(grid):
    # find all 3x3 subgrids that are a single non-zero color
    solid_color_subgrids = []
    for r in range(grid.shape[0] - 2):
        for c in range(grid.shape[1] - 2):
            subgrid = grid[r:r+3, c:c+3]
            unique_colors = np.unique(subgrid)
            if len(unique_colors) == 2 and 0 in unique_colors:
                solid_color_subgrids.append(subgrid)
            elif len(unique_colors) == 1 and unique_colors[0] != 0:
                solid_color_subgrids.append(subgrid)
    return solid_color_subgrids

def transform(input_grid):
    # convert to numpy array
    input_grid = np.array(input_grid)
    
    # find all solid color subgrids
    solid_color_subgrids = find_solid_color_subgrids(input_grid)
    
    # construct output (use first one found - may need refinement later)
    if len(solid_color_subgrids) > 0:
        output_grid = solid_color_subgrids[0].tolist()
    else:
        output_grid = [] # default to empty if not found
    
    return output_grid
```
