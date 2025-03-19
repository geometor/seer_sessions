# 0ca9ddb6 • 018 • refine_coder

---
```python
"""
1.  **Identify contiguous regions** of blue (1), red (2), and magenta (6) pixels in the input grid.
2.  **For each blue region:** Create orange (7) pixels in all cells directly adjacent (up, down, left, right, and diagonals) to *any* pixel in the blue region.
3.  **For each red region:** Create yellow (4) pixels in all cells directly adjacent (up, down, left, and right, but *not* diagonal) to *any* pixel in the red region.
4. **For each magenta Region:** Do not add any new pixels.
5.  **Preserve** all original pixels in the input grid, including those within the identified regions.
6.  **Return** the modified grid.
"""

import numpy as np
from scipy.ndimage import label

def get_regions(grid, color):
    """Identifies contiguous regions of a specific color in the grid."""
    colored_mask = (grid == color).astype(int)
    labeled_array, num_features = label(colored_mask)
    regions = []
    for i in range(1, num_features + 1):  # Iterate through each labeled region
        region_coords = np.where(labeled_array == i)
        regions.append(list(zip(region_coords[0], region_coords[1])))
    return regions

def get_all_adjacent_coords(region, grid_shape):
    """Gets all valid adjacent coordinates (including diagonals) for a region."""
    rows, cols = grid_shape
    all_adjacent = set()
    for r, c in region:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the cell itself
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    all_adjacent.add((nr, nc))
    return list(all_adjacent)

def get_cross_adjacent_coords(region, grid_shape):
    rows,cols = grid_shape
    all_adjacent = set()
    for r, c in region:
        if r > 0:
            all_adjacent.add((r-1,c)) # up
        if r < rows-1:
            all_adjacent.add((r+1, c)) # down
        if c > 0:
            all_adjacent.add((r,c-1)) #left
        if c < cols-1:
            all_adjacent.add((r, c+1)) # right

    return list(all_adjacent)

def transform(input_grid):
    # Initialize output grid with the same values as the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify regions of each color
    blue_regions = get_regions(input_grid, 1)
    red_regions = get_regions(input_grid, 2)
    magenta_regions = get_regions(input_grid, 6)

    # Apply transformations for each blue region
    for region in blue_regions:
        adjacent_coords = get_all_adjacent_coords(region, (rows, cols))
        for nr, nc in adjacent_coords:
            output_grid[nr, nc] = 7  # Orange

    # Apply transformations for each red region
    for region in red_regions:
        adjacent_coords = get_cross_adjacent_coords(region, (rows,cols))
        for nr, nc in adjacent_coords:
            output_grid[nr, nc] = 4  # Yellow
    
    # magenta regions have no effect

    return output_grid
```
