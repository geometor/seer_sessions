```python
"""
The transformation involves a series of color expansions, some of which are localized (top/bottom halves of the grid) and some are global. The expansion of a color is defined by what colors it can overwrite and what colors stop it.

1.  **Local Expansions (Top/Bottom Half):**
    *   If the top half contains color 3 (green), expand color 3 upwards, overwriting color 0 (white), and stopping at colors 1, 2, 4, 5, 6, 7, 8, and 9.
    *   If the top half contains color 4 (yellow), expand color 4 upwards, overwriting color 0, and stopping at colors 1, 2, 3, 5, 6, 7, 8, and 9.
    * If the bottom half contains color 6(magenta) and 7(orange), expand the region of 6, overwriting 0 and stopping at colors 1, 2, 3, 4, 5, 7, 8 and 9. Within the expanded region of 6, expand 7 overwriting 0 and 6, stopping at colors 1, 2, 3, 4, 5, 8 and 9.
    *   If the bottom half contains color 7 (orange) *without* color 6, expand color 7, overwriting color 0 and stopping at colors 1, 2, 3, 4, 5, 6, 8 and 9.

2.  **Global Expansions:**
    *   Expand color 5 (gray), overwriting color 0 (white) and stopping at colors 1, 2, 3, 4, 6, 7, 8, and 9.
    *   Expand color 6 (magenta), overwriting colors 0, 3, 4, 5, 7, 8, and 9, and stopping at colors 1 and 2.
    *   Expand color 9 (maroon), overwriting colors 0, 4, 5, 6, 7, and 8, and stopping at colors 1, 2, and 3.

3.  **Masked Expansion**
     * If color 3 and 5 are both in the output: Expand color 3, overwriting colors 0 and 5, and stopping at colors at 1, 2, 4, 6, 7, 8 and 9. *Only* expand color 3 *within* regions that were previously color 5.

4. Order of operations: Local top, Local bottom, Global 5, Global 6, Global 9, Masked 3.
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
     for region in regions:
        expanded = expand_region(grid, region, fill_color, overwrite_colors, stop_colors)
        for r, c in expanded:
            if mask[r,c]:
                output_grid[r,c] = fill_color
     return output_grid


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Local Expansions (Top/Bottom Half)
    # Top half: Expand 3 upwards
    output_grid = apply_transformation_pass(output_grid, 3, 3, [0], [1, 2, 4, 5, 6, 7, 8, 9], local_region="top_half")
    # Top half: Expand 4 upwards
    output_grid = apply_transformation_pass(output_grid, 4, 4, [0], [1, 2, 3, 5, 6, 7, 8, 9], local_region="top_half")

    # Bottom half: Expand 6, then 7 within 6 (if both present)
    if 6 in output_grid[rows // 2:, :] and 7 in output_grid[rows // 2:, :]:
        output_grid = apply_transformation_pass(output_grid, 6, 6, [0], [1, 2, 3, 4, 5, 7, 8, 9], local_region="bottom_half")
        output_grid = apply_masked_expansion(output_grid, 7, 6, [0, 6], [1, 2, 3, 4, 5, 8, 9])

    # Bottom half: Expand 7 (if 6 is not present)
    elif 7 in output_grid[rows // 2:, :]:
        output_grid = apply_transformation_pass(output_grid, 7, 7, [0], [1, 2, 3, 4, 5, 6, 8, 9], local_region="bottom_half")

    # 2. Global Expansions
    output_grid = apply_transformation_pass(output_grid, 5, 5, [0], [1, 2, 3, 4, 6, 7, 8, 9])  # Expand 5
    output_grid = apply_transformation_pass(output_grid, 6, 6, [0, 3, 4, 5, 7, 8, 9], [1, 2])  # Expand 6
    output_grid = apply_transformation_pass(output_grid, 9, 9, [0, 4, 5, 6, 7, 8], [1, 2, 3])  # Expand 9

    # 3. Masked expansion
    output_grid = apply_masked_expansion(output_grid, 3, 5, [0,5], [1,2,4,6,7,8,9])

    return output_grid.tolist()
```