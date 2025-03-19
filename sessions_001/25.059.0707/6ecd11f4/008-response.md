# 6ecd11f4 • 008 • refine_coder

---
```python
"""
1.  **Identify Target Region:** Locate a distinct 3x3 colored square region within the input grid. This region can have any color as its primary component (excluding the background).
2.  **Extract Subgrid:** Extract the 3x3 region identified.
3.  **Conditional Reduction**: If the background is not blue(1) or gray (5), extract the 3x3 grid. If the background is blue(1), extract the middle row. If the background is gray(5), extract the middle row.
"""

import numpy as np

def find_3x3_subgrid(grid):
    """Finds the 3x3 subgrid with distinct colors."""
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = grid[r:r+3, c:c+3]
            unique_colors = np.unique(subgrid)
            # Check if the subgrid contains other colors than the background
            if len(unique_colors) > 1: # Simplest way to ensure its a mixed color subgrid
               return r, c
    return None, None

def get_background_color(grid):
    """Determine the most frequent color, considered the background"""
    unique_colors, counts = np.unique(grid, return_counts=True)
    # Exclude subgrids with no background, which would be a count of 9.
    if len(counts) > 1:
        background_color = unique_colors[np.argmax(counts)]
        return background_color
    else: 
        return None

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify Target Region and Extract Subgrid
    start_row, start_col = find_3x3_subgrid(input_grid)
    
    if start_row is None or start_col is None:
        return [[]] # Return Empty grid if no 3x3 is found

    output_grid = input_grid[start_row:start_row+3, start_col:start_col+3].copy()
    
    # 2. Conditional Reduction.
    background_color = get_background_color(input_grid)
    
    if background_color == 1:
       output_grid = output_grid[1:2, :] # Extract middle row
    elif background_color == 5:
        output_grid = output_grid[1:2, :] # Extract the middle row
    # else: return the entire subgrid

    return output_grid.tolist()
```
