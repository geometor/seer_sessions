```python
"""
Transforms input grids by performing a series of region expansions. The
transformations can be local (top/bottom halves) or global, with specific rules
for each color regarding what it can overwrite and what colors stop its
expansion. The order of expansions is important and can vary between examples.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a given color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(row, col):
        """Depth-first search to find contiguous region."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                regions.append(dfs(r, c))
    return regions

def expand_region(grid, region, fill_color, overwrite_colors, stop_colors):
    """Expands a region, replacing specified colors and stopping at others."""
    expanded_region = set(region)  # Use a set for efficient membership checking
    queue = region[:]
    rows, cols = grid.shape

    while queue:
        row, col = queue.pop(0)
        # Consider neighbors (up, down, left, right)
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in expanded_region):
                pixel_color = grid[nr, nc]
                if pixel_color in overwrite_colors:
                    expanded_region.add((nr, nc))
                    queue.append((nr, nc))
                elif pixel_color in stop_colors:  #stop the spread, dont add to queue
                    continue

    return list(expanded_region)

def apply_transformation_pass(input_grid, anchor_color, fill_color, overwrite_colors, stop_colors):
    """Applies a single pass of the transformation, expanding from anchor color."""
    output_grid = np.copy(input_grid)
    anchor_regions = find_regions(input_grid, anchor_color)

    for region in anchor_regions:
      expanded = expand_region(input_grid, region, fill_color, overwrite_colors, stop_colors)
      for r, c in expanded:
        output_grid[r,c] = fill_color

    return output_grid


def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Check for top/bottom split behavior (Examples 1 and 4)
    top_half = input_grid[:rows // 2, :]
    bottom_half = input_grid[rows // 2:, :]

    # Example 1: Green (3) expands upwards in the top half.
    if 3 in top_half and not np.array_equal(top_half, apply_transformation_pass(top_half, 3, 3, [0], [1, 2])):
        output_grid[:rows // 2, :] = apply_transformation_pass(top_half, 3, 3, [0], [1, 2,4,5,6,7,8,9])

    # Example 4: Green(3) and Yellow(4)
    if 3 in top_half:
      output_grid[:rows // 2, :] = apply_transformation_pass(top_half, 3, 3, [0], [1, 2,4,5,6,7,8,9])
    if 4 in top_half:
      output_grid[:rows // 2, :] = apply_transformation_pass(top_half, 4, 4, [0], [1, 2,3,5,6,7,8,9])

    # example 4: color 7 within color 6 region
    if 6 in bottom_half and 7 in bottom_half:
        # First expand 6 in the bottom half
        bottom_half_expanded_6 = apply_transformation_pass(bottom_half, 6, 6, [0], [1,2,3,4,5,7,8,9])

        # Create a mask for the expanded 6 region
        mask_6 = (bottom_half_expanded_6 == 6)

        # Expand 7, but only within the masked region
        bottom_half_expanded_7 = np.copy(bottom_half_expanded_6)
        regions_7 = find_regions(bottom_half, 7) #find initial regions
        for region in regions_7:
           expanded_7 = expand_region(bottom_half_expanded_6, region, 7, [0,6], [1,2,3,4,5,8,9]) # expand
           for r, c in expanded_7:  # apply expansion based on mask
              if mask_6[r,c]:
                bottom_half_expanded_7[r, c] = 7  # only change where it was 6

        output_grid[rows // 2:, :] = bottom_half_expanded_7

    elif 7 in bottom_half: # example 1, bottom half has 3
        output_grid[rows // 2:, :] = apply_transformation_pass(bottom_half, 7, 7, [0], [1,2,3,4,5,6,8,9])

    # 2. Example 2: color 5 expands to fill adjacent 0
    output_grid = apply_transformation_pass(output_grid, 5, 5, [0], [1,2,3,4,6,7,8,9]) # expand 5 to fill adjacent

    # 3. Global operations (Example 3) - Apply *after* local expansions
    # example 3: Color 6 first, overwrites all except 1 and 2
    output_grid = apply_transformation_pass(output_grid, 6, 6, [0,3,4,5,7,8,9], [1,2])
    # example 3: Color 9 second, overwrites all except 1, 2, and 3
    output_grid = apply_transformation_pass(output_grid, 9, 9, [0,4,5,6,7,8], [1,2,3])


    # 4. Example 2: Color 3 (green) expands inside color 5
    if 3 in output_grid and 5 in output_grid:
        mask_5 = (output_grid == 5)  # Create color 5 mask
        output_grid_expanded_3 = np.copy(output_grid)
        regions_3 = find_regions(output_grid, 3)  # Find color 3 initial regions

        for region in regions_3:
           expanded_3 = expand_region(output_grid, region, 3, [0,5], [1,2,4,6,7,8,9]) #expand 3
           for r,c in expanded_3:
              if mask_5[r,c]:
                output_grid_expanded_3[r,c]=3

        output_grid = output_grid_expanded_3


    return output_grid.tolist()
```