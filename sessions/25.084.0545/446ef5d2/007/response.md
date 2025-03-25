```python
"""
1.  **Identify Background:** The background color is consistently color '8' (azure).
2.  **Identify Enclosed Regions:** Find all distinct regions enclosed by the background color.  These regions are completely surrounded by the background color and do not touch the edges of the entire grid.  Each enclosed region should be treated independently.
3.  **Identify Objects:** Within each enclosed region, identify "objects." An object is a group of connected pixels (horizontally, vertically, or diagonally) that share the same color and are *not* the background color.
4.  **Gravity within Regions:**  For each enclosed region, apply a "gravity" effect.  All objects within the region fall downwards.  The movement stops when an object hits:
    *   The bottom boundary of its enclosed region.
    *   Another object within the same region.
5. **Preserve Boundaries:** The surrounding boundary of azure (8) must remain unchanged.
"""

import numpy as np

def find_objects(grid, region_mask):
    """Finds contiguous regions (objects) of the same color within a region."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or not region_mask[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and region_mask[row, col] and grid[row,col] != 8:  # Ensure we stay within the region
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects.append({'color': grid[row, col], 'pixels': object_pixels})
    return objects

def find_enclosed_regions(grid, background_color):
    """Finds regions enclosed by the background color."""
    # Invert the background to find non-background areas
    non_background_mask = grid != background_color

    # Use a flood-fill algorithm to identify regions connected to the border
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or not non_background_mask[r, c]):
            return
        visited[r, c] = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                dfs(r + dr, c + dc)

    # Mark all non-background pixels connected to the edges as visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if non_background_mask[r,c]:
                dfs(r,c)
    for c in range(cols):
      for r in [0, rows -1]:
        if non_background_mask[r,c]:
            dfs(r,c)

    # The enclosed regions are the non-visited, non-background pixels
    enclosed_mask = np.logical_and(non_background_mask, ~visited)
    return enclosed_mask


def shift_objects_in_region(grid, region_mask, background_color):
    """Shifts objects down within a specific region."""
    # Create a copy to work on
    grid_copy = np.copy(grid)
    objects = find_objects(grid_copy, region_mask)

    # Clear the original object positions within this region
    for obj in objects:
      for r, c in obj['pixels']:
        if region_mask[r,c]: # only clear if inside the region
          grid_copy[r,c] = background_color

    # Move each object within the region
    for obj in objects:
        pixels = obj['pixels']
        pixels.sort(key=lambda p: p[0], reverse=True)  # Sort by row, descending
        color = obj['color']

        for r, c in pixels:
            new_r = r
            # Move down until blocked by boundary or another object
            while (new_r + 1 < grid.shape[0] and region_mask[new_r + 1, c] and
                   grid_copy[new_r + 1, c] == background_color ):
                new_r += 1
            grid_copy[new_r, c] = color
            
    return grid_copy


def transform(input_grid):
    # 1. Identify Background
    background_color = 8
    output_grid = np.copy(input_grid)

    # 2. Identify Enclosed Regions
    enclosed_regions_mask = find_enclosed_regions(output_grid, background_color)

    # Get all the individual enclosed region masks
    visited = np.zeros_like(enclosed_regions_mask, dtype=bool)
    regions = []

    def dfs_regions(row,col,current_region):
        if(row < 0 or row >= enclosed_regions_mask.shape[0] or col < 0 or col >= enclosed_regions_mask.shape[1]
          or visited[row,col] or not enclosed_regions_mask[row,col]):
            return

        visited[row,col] = True
        current_region.append((row,col))
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue;
                dfs_regions(row+dr,col+dc,current_region)



    for row in range(enclosed_regions_mask.shape[0]):
        for col in range(enclosed_regions_mask.shape[1]):
            if enclosed_regions_mask[row,col] and not visited[row,col]:
                current_region = []
                dfs_regions(row,col,current_region)
                regions.append(current_region)
    

    # 3. & 4. Process Each Region and Shift Objects
    for region_pixels in regions:
        # create region mask for current region
        region_mask = np.zeros_like(output_grid, dtype = bool)
        for r,c in region_pixels:
            region_mask[r,c] = True

        output_grid = shift_objects_in_region(output_grid, region_mask, background_color)

    return output_grid
```