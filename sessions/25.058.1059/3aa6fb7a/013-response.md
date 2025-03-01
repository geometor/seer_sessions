# 3aa6fb7a • 013 • refine_coder

---
```python
"""
1.  **Contextual Row Duplication/Insertion:**
    *   Examine the input grid. Identify contiguous regions of the same color.
    *   *If* the entire grid consists of only azure pixels, duplicate every other row, and insert a blue horizontal line within the expanded azure lines.
2. **Grey Influence:**
    * *If* a grey area is present to left of an azure area, change specific azure pixels.
    * Identify every other row within the azure region.
    * *If* those identified rows are also adjacent to the grey vertical region, insert blue pixels there.
3.  **Preservation:**
    *   *If* no specific conditions for azure pixel modification or row duplication are met (as in Example 1), preserve the original grid without changes.
4. **Note**: This is more complex because it appears to be a state based transformation, not just a simple rule.
"""

import numpy as np

def duplicate_every_other_row_with_blue(grid):
    """Duplicates every other row of the input grid and inserts a blue line."""
    rows, cols = grid.shape
    new_rows = []
    for i in range(rows):
        new_rows.append(grid[i].copy())
        if (i + 1) % 2 == 0:  # Duplicate every other row, starting with the second
            new_row = grid[i].copy()
            new_rows.append(new_row) # duplicate original
            new_blue_row = np.ones(cols, dtype=int) # make a blue row
            new_rows.append(new_blue_row) #add a blue row.
           
    return np.array(new_rows)

def insert_blue_adjacent_to_grey(grid):
    """Inserts blue pixels in azure regions adjacent to a grey vertical bar."""
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    for row in range(rows):
        for col in range(cols):
            if (row+1) % 2 == 0: # every other row
              if grid[row,col] == 8: # if azure
                if col > 0 and grid[row,col-1] == 5: # if grey to left
                    output_grid[row,col] = 1 # make blue

    return output_grid
    
def check_all_azure(grid):
  """check if entire grid is azure"""
  rows, cols = grid.shape
  for row in range(rows):
    for col in range(cols):
        if grid[row,col] != 8:
            return False # found non-azure

  return True


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # check for all azure
    all_azure = check_all_azure(input_grid)

    # duplicate every other row with blue insert
    if all_azure:
        output_grid = duplicate_every_other_row_with_blue(input_grid)
        return output_grid # early return

    # grey influence
    output_grid = insert_blue_adjacent_to_grey(output_grid)

    return output_grid
```
