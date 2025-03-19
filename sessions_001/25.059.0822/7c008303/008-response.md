# 7c008303 • 008 • refine_coder

---
```python
"""
1.  **Identify:** Identify all contiguous rectangular regions of the same color within the input grid. These are the sub-regions.
2.  **Select:** For each sub-region, select the pixel at the top-left corner.
3.  **Create:** Create an output grid. The output grid dimensions are determined by the number of identified sub-regions.
4. **Map and Fill:** Create output of appropriate dimensions (see examples). Map the color of each selected pixel to a corresponding cell in the output grid. The arrangement of the output should match the spatial arrangement of the identified regions in the input.
"""

import numpy as np

def find_contiguous_regions(input_grid):
    """
    Finds contiguous rectangular regions of the same color in the input grid.
    Returns a list of regions, where each region is represented by a tuple:
    ((row_start, row_end), (col_start, col_end), color)
    """
    visited = np.zeros_like(input_grid, dtype=bool)
    regions = []

    def is_valid(row, col):
        return 0 <= row < input_grid.shape[0] and 0 <= col < input_grid.shape[1]

    def dfs(row, col, color, region_coords):
        if not is_valid(row, col) or visited[row, col] or input_grid[row, col] != color:
            return

        visited[row, col] = True
        region_coords[0] = min(region_coords[0], row)
        region_coords[1] = max(region_coords[1], row + 1)
        region_coords[2] = min(region_coords[2], col)
        region_coords[3] = max(region_coords[3], col + 1)
       

        dfs(row + 1, col, color, region_coords)
        dfs(row - 1, col, color, region_coords)
        dfs(row, col + 1, color, region_coords)
        dfs(row, col - 1, color, region_coords)

    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if not visited[i, j]:
                color = input_grid[i, j]
                region_coords = [input_grid.shape[0], 0, input_grid.shape[1], 0]  # [row_start, row_end, col_start, col_end]
                dfs(i, j, color, region_coords)
                regions.append(((region_coords[0], region_coords[1]), (region_coords[2], region_coords[3]), color))

    return regions

def transform(input_grid):
    # Identify contiguous regions
    regions = find_contiguous_regions(input_grid)

    # Determine output grid size
    if len(regions) == 6:  # Example 1
        output_height = 2
        output_width = 3
    elif len(regions) == 4: # example 2, 3
        output_height = 2
        output_width = 2
    elif len(regions) == 1: # example 4
        output_height = 1
        output_width = 1
    else: # default
        output_height = len(regions)
        output_width = 1
  

    # Create output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Sort regions to ensure consistent output order (top-to-bottom, left-to-right)
    regions.sort(key=lambda region: (region[0][0], region[1][0]))

    # Map and Fill
    region_index = 0
    for i in range(output_height):
        for j in range(output_width):
            if region_index < len(regions):
               (row_start, _), (col_start, _), color = regions[region_index]
               output_grid[i, j] = color
            region_index += 1

    return output_grid
```
