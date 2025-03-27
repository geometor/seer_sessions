```python
"""
The transformation involves a series of color expansions, with specific rules and order of operations for each color.

1.  **Initial Setup:**
    *   The input grid is the starting point.

2.  **Ordered Expansions:** Apply the following expansions *in the specified order*:

    a. **Top Half Expansions** (only consider the top half of grid)
        *   If color `3` (green) is present, expand it upwards, overwriting `0` (white), and stopping at any other color.
        *   If color `4` (yellow) is present, expand it upwards, overwriting `0` (white), and stopping at any other color.
    b. **Bottom Half Expansions** (only consider the bottom half of the grid)
        *    If colors `6` (magenta) and `7` (orange) are both present:
            *   Expand color `6` (magenta), overwriting `0` and stop at any other color except 6.
            *   Within the expanded `6` region, expand `7` (orange) overwriting `0` and `6`. Stop at any other color.
        *   If only `7` (orange) is present (no `6`): Expand `7` overwriting `0` and stop at any other color.
    c. **Global Expansions (consider the entire grid)**:
       *  Expand color 5 (gray) to fill all areas where there are 0s.
       * Expand color 6 (magenta), overwriting `0`, `3`, `4`, `5`, `7`, `8`, and `9`, stopping at `1` and `2`.
       * Expand color `9` (maroon), overwriting `0`, `2`, and `4`, stopping at `1`, `3`.
       * Expand color `3` (green) *only within the regions where color 5 (gray) was present* in the input. Color `3` overwrites `0` and `5` and stops at all others.

3.  **Notes and Interactions:**

    *   The order of expansions is *critical*.
    *   "Expand" means to replace neighboring pixels of the specified "overwrite" colors with the expanding color.
    *   "Stopping at" a color means the expansion does *not* replace that color.
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
    expanded_region = set(region)
    queue = region[:]
    rows, cols = grid.shape

    while queue:
        row, col = queue.pop(0)
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in expanded_region):
                pixel_color = grid[nr, nc]
                if pixel_color in overwrite_colors:
                    expanded_region.add((nr, nc))
                    queue.append((nr, nc))
                elif pixel_color in stop_colors:
                    continue

    return list(expanded_region)

def apply_transformation_pass(input_grid, anchor_color, fill_color, overwrite_colors, stop_colors, local_region=None):
    """Applies a single pass of the transformation, expanding from anchor color."""
    output_grid = np.copy(input_grid)
    if local_region == "top_half":
        grid_slice = output_grid[:output_grid.shape[0] // 2, :]
    elif local_region == "bottom_half":
        grid_slice = output_grid[output_grid.shape[0] // 2:, :]
    else:
        grid_slice = output_grid

    anchor_regions = find_regions(grid_slice, anchor_color)

    for region in anchor_regions:
      expanded = expand_region(grid_slice, region, fill_color, overwrite_colors, stop_colors)
      for r, c in expanded:
          if local_region == "top_half":
              output_grid[r,c] = fill_color #no offset needed
          elif local_region == "bottom_half":
              output_grid[r + output_grid.shape[0] // 2, c] = fill_color
          else:
            output_grid[r,c] = fill_color

    return output_grid

def apply_masked_expansion(grid, fill_color, mask_color, overwrite_colors, stop_colors):
     """Expands fill_color within the mask, overwriting specified colors."""
     output_grid = np.copy(grid)
     mask = (grid == mask_color)
     regions = find_regions(grid, fill_color)

     # Get initial regions of the mask color.
     initial_mask_regions = find_regions(grid, mask_color)
     initial_mask_coords = set()
     for region in initial_mask_regions:
          initial_mask_coords.update(region)


     for region in regions:
        expanded = expand_region(grid, region, fill_color, overwrite_colors, stop_colors)
        for r, c in expanded:
            # Only fill if the coordinate was originally part of the mask
            if (r,c) in initial_mask_coords:
                output_grid[r,c] = fill_color
     return output_grid


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    initial_grid = np.copy(input_grid) # for masked expansion later

    # 2. Ordered Expansions
    # a. Top Half Expansions
    output_grid = apply_transformation_pass(output_grid, 3, 3, [0], [1, 2, 4, 5, 6, 7, 8, 9], local_region="top_half")
    output_grid = apply_transformation_pass(output_grid, 4, 4, [0], [1, 2, 3, 5, 6, 7, 8, 9], local_region="top_half")

    # b. Bottom Half Expansions
    if 6 in output_grid[rows // 2:, :] and 7 in output_grid[rows // 2:, :]:
        output_grid = apply_transformation_pass(output_grid, 6, 6, [0], [1, 2, 3, 4, 5, 7, 8, 9], local_region="bottom_half")
        output_grid = apply_masked_expansion(output_grid, 7, 6, [0, 6], [1, 2, 3, 4, 5, 8, 9])
    elif 7 in output_grid[rows // 2:, :]:
         output_grid = apply_transformation_pass(output_grid, 7, 7, [0], [1, 2, 3, 4, 5, 6, 8, 9], local_region="bottom_half")

    # c. Global Expansions
    output_grid = apply_transformation_pass(output_grid, 5, 5, [0], [1, 2, 3, 4, 6, 7, 8, 9])
    output_grid = apply_transformation_pass(output_grid, 6, 6, [0, 3, 4, 5, 7, 8, 9], [1, 2])
    output_grid = apply_transformation_pass(output_grid, 9, 9, [0, 2, 4], [1, 3]) #corrected overwrite colors
    # Masked expansion of 3, using the *initial* grid's color 5 locations.
    output_grid = apply_masked_expansion(initial_grid, 3, 5, [0, 5], [1, 2, 4, 6, 7, 8, 9])

    return output_grid.tolist()
```