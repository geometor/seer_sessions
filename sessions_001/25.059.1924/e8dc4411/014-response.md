# e8dc4411 • 014 • refine_coder

---
```python
"""
Identify all contiguous regions of green pixels in the input grid and expand
them downwards to the bottom of the grid, maintaining the original width of
each region. If a green region is a single pixel, extend it downward by one.
"""

import numpy as np

def get_green_regions(grid):
    """Identifies contiguous regions of green pixels."""
    green_coords = np.argwhere(grid == 3)
    regions = []
    visited = set()

    def is_adjacent(coord1, coord2):
        """Checks if two coordinates are adjacent (horizontally or vertically)."""
        return (abs(coord1[0] - coord2[0]) <= 1 and coord1[1] == coord2[1]) or \
               (abs(coord1[1] - coord2[1]) <= 1 and coord1[0] == coord2[0])

    def dfs(coord, current_region):
        """Depth-first search to find all connected green pixels."""
        visited.add(tuple(coord))
        current_region.append(coord)
        for other_coord in green_coords:
            if tuple(other_coord) not in visited and is_adjacent(coord, other_coord):
                dfs(other_coord, current_region)

    for coord in green_coords:
        if tuple(coord) not in visited:
            current_region = []
            dfs(coord, current_region)
            regions.append(current_region)

    return regions

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all green regions
    green_regions = get_green_regions(input_grid)
    
    # Expand each green region downwards
    for region in green_regions:
        # Get the columns occupied by the region
        cols = sorted(list(set([coord[1] for coord in region])))
        
        #find the highest row
        topmost_row = min(coord[0] for coord in region)
        
        if len(region) == 1:
            #if only 1 pixel, extend it by 1
            if topmost_row + 1 < output_grid.shape[0]:
                output_grid[topmost_row + 1, cols[0]] = 3
        else:        
            #expand down
            for row in range(topmost_row, output_grid.shape[0]):
                for col in cols:
                    output_grid[row, col] = 3

    return output_grid
```
