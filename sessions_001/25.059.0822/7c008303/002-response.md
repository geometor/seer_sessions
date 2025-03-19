# 7c008303 • 002 • example_3 • investigate_coder

---
```python
"""
The input grid is transformed into a smaller output grid. A horizontal azure (8) line in the input separates colored regions.
Each region above and below the azure line is reduced to a 2x2 block of the same color in the output, maintaining relative position and the original color.
if next to grid boundary, draw line of length two toward interior, if at a corner, place a single pixel.
"""

import numpy as np

def find_azure_line(grid):
    # Find the row index of the horizontal azure line.
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1  # Should not happen based on problem description

def get_regions(grid, azure_line_row):
    # Identify distinct colored regions above and below the azure line.
    visited = set()
    regions = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, region_set):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        region_set.add((r, c))

        # Explore adjacent cells (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color, region_set)
    
    above_regions = []
    for r in range(0, azure_line_row):
        for c in range(grid.shape[1]):
             if (r,c) not in visited and grid[r, c] != 8 and grid[r,c] != 0:
                new_region = set()
                dfs(r, c, grid[r, c], new_region)
                if new_region:
                    above_regions.append((grid[r,c],new_region))
    
    visited = set() # reset visited for below regions
    below_regions = []
    for r in range(azure_line_row + 1, grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r,c) not in visited and grid[r, c] != 8 and grid[r,c] != 0:
                new_region = set()
                dfs(r, c, grid[r, c], new_region)
                if new_region:
                    below_regions.append((grid[r,c], new_region))

    return above_regions, below_regions

def get_top_left(region):
  min_r = min(r for r,c in region)
  min_c = min(c for r,c in region if r == min_r)
  return (min_r, min_c)
  

def transform(input_grid):
    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Find the azure line
    azure_line_row = find_azure_line(grid)

    # Get regions above and below the azure line
    above_regions, below_regions = get_regions(grid, azure_line_row)
    
    # compute output grid dimension.  +1 if there are regions below
    output_height = (len(above_regions) + len(below_regions)) 
    if len(below_regions) > 0:
      output_height = max(len(above_regions),len(below_regions)) * 2

    output_width = 0
    if len(above_regions) > 0:
        output_width = max(output_width, len(above_regions)*2)
    if len(below_regions) > 0:
        output_width = max(output_width, len(below_regions)*2)
        
    if (output_width == 0):
        output_width = grid.shape[1] // 2
    
    
    
    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Process above regions
    for i, (color, region) in enumerate(above_regions):
      r,c = get_top_left(region)
      out_r = (r * 2 ) // (azure_line_row+1)
      out_c = (c * 2) // (grid.shape[1]+1)
      if out_r+1 < output_grid.shape[0] and out_c+1 < output_grid.shape[1]:
        output_grid[out_r:out_r+2, out_c:out_c+2] = color
      elif out_r+1 < output_grid.shape[0]:
        output_grid[out_r:out_r+2, out_c] = color
      elif out_c+1 < output_grid.shape[1]:
        output_grid[out_r, out_c:out_c+2] = color
      else:
        output_grid[out_r,out_c] = color

    # Process below regions
    for i, (color, region) in enumerate(below_regions):
        r,c = get_top_left(region)
        #out_r = (r * output_height) // grid.shape[0]
        #out_c = (c * output_width) // grid.shape[1]
        out_r = ((r-azure_line_row-1) * 2 ) // (grid.shape[0]-azure_line_row)  + (output_height//2)
        out_c = (c * 2) // (grid.shape[1]+1)
        if out_r+1 < output_grid.shape[0] and out_c+1 < output_grid.shape[1]:
            output_grid[out_r:out_r+2, out_c:out_c+2] = color
        elif out_r+1 < output_grid.shape[0]:
            output_grid[out_r:out_r+2, out_c] = color
        elif out_c+1 < output_grid.shape[1]:
            output_grid[out_r, out_c:out_c+2] = color
        else:
            output_grid[out_r,out_c] = color


    return output_grid.tolist()
```
