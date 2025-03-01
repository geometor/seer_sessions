# 56dc2b01 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying green (3) and red (2) regions in the input, moving them down,
and inserting a horizontal azure (8) line above them.
"""

import numpy as np

def find_regions(grid, color):
    # Find contiguous regions of a specific color
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(r, c, current_region):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != color
        ):
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def find_lowest_row(grid):
    # Find lowest row
    rows, _ = grid.shape
    for r in range(rows - 1, -1, -1):
        if np.any(grid[r] != 0):
            return r
    return -1

def find_highest_row(grid):
   # find the highest row containing existing elements
    for r, row in enumerate(grid):
        if np.any(row != 0):
            return r
    return 0


def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find green and red regions
    green_regions = find_regions(input_grid, 3)
    red_regions = find_regions(input_grid, 2)
    
    # find lowest and higest existing row
    lowest_row = find_lowest_row(input_grid)
    highest_row = find_highest_row(input_grid)


    # determine azure line row
    if lowest_row == -1:
       azure_row = 0
    else:
      # if any row exist under the green and red object
      if any(r >  max(max(gr, key=lambda item: item[0])[0] for gr in green_regions) if len(green_regions) > 0 else 0, max(rr, key=lambda item: item[0])[0] for rr in red_regions if len(red_regions) > 0 else 0 for r,_ in np.ndindex(input_grid.shape)):
        azure_row = highest_row -1 if highest_row > 0 else 0
      else:
       azure_row = lowest_row+1
    
    
    # insert any existing content on top of new content
    offset = azure_row + 1
  
    
    # find if any elements exists and copy to a position under azure line
    if lowest_row != -1:
        rows, cols = input_grid.shape
        for r in range(rows):
          for c in range(cols):
            if input_grid[r,c] != 0 and input_grid[r,c] != 2 and input_grid[r,c] != 3 and input_grid[r,c] != 8:
                if r < highest_row:
                  output_grid[r + offset,c ] = input_grid[r,c]
                else:

                  output_grid[r ,c] = input_grid[r,c]


    # Create azure line
    if azure_row >= 0 and azure_row < output_grid.shape[0]:
        output_grid[azure_row, :] = 8


    # Calculate row offset for moving green and red regions, offset based on azure
    row_offset = azure_row+1

    # Move green regions
    for region in green_regions:
        for r, c in region:
            new_r = r + row_offset
            if new_r < output_grid.shape[0]:  # Ensure within bounds
               output_grid[new_r, c] = 3

    # Move red regions, offset by same amount.
    for region in red_regions:
        for r, c in region:
            new_r = r + row_offset
            if new_r < output_grid.shape[0]:  # Ensure within bounds
                output_grid[new_r, c] = 2

    return output_grid
```
