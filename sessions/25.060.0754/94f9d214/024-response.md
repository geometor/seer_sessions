# 94f9d214 • 024 • refine_coder

---
```python
"""
1.  **Locate Trigger:** Examine the input grid. If there is a region that meets one of the following criteria, continue to Action.
    *   a 3x1 block of blue (1).
    *   a 1x3 block of blue (1).
    *   a 2x2 block of blue (1).
2.  **Action:**
    1.  **Extract:** Extract the 4x4 subgrid from the top-left corner of the input grid.
    2.  **Transform:** Within this 4x4 subgrid:
        *   Change all occurrences of '3' (green) to '2' (red).
        *   Change all occurances of '1' (blue) to '0' (white).
3.  **Output:** The transformed 4x4 subgrid is the output.
"""

import numpy as np

def find_blue_blocks(grid):
    """
    Searches for 3x1, 1x3, or 2x2 blocks of blue (1) within the grid.
    Returns True if any such block is found, False otherwise.
    """
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols):
            if grid[i:i+3, j].sum() == 3 and np.all(grid[i:i+3, j] == 1):  # 3x1 block
                return True
    for i in range(rows):
        for j in range(cols - 2):
            if grid[i, j:j+3].sum() == 3 and np.all(grid[i, j:j+3] == 1):  # 1x3 block
                return True
    for i in range(rows - 1):
        for j in range(cols - 1):
            if grid[i:i+2, j:j+2].sum() == 4 and np.all(grid[i:i+2, j:j+2] == 1):  # 2x2 block
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Locate Trigger: Check for the presence of blue blocks.
    if find_blue_blocks(input_grid):
        # Action: Extract the 4x4 subgrid.
        subgrid = input_grid[:4, :4]
        output_grid = np.copy(subgrid)

        # Transform: Change 3 to 2 and 1 to 0 within the subgrid.
        output_grid[output_grid == 3] = 2
        output_grid[output_grid == 1] = 0
    else:
        # If no trigger, return an empty grid (or potentially a copy of the input).
        # For now, returning an empty 4x4 grid filled with 0s
        output_grid = np.zeros((4,4),dtype=int)

    return output_grid
```

