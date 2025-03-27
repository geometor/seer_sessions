"""
The transformation removes all white (0) pixels from the input grid and stacks the remaining colored regions on top of each other, maintaining their original horizontal positions. The colored regions maintain relative x-coordinates, creating subgrids. The order of subgrids is given by the numerical value. Magenta sections are also completely removed.
"""

import numpy as np

def identify_regions(grid):
    """
    Identifies contiguous regions of non-zero, non-six colored pixels in the grid,
    treating vertically separated regions of the same color as distinct.
    """
    grid = np.array(grid)
    regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, region):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color or grid[r, c] == 6:
            return
        visited[r, c] = True
        region.append((r, c))
        # Only check horizontally adjacent cells
        for dr, dc in [(0, 1), (0, -1)]:
            dfs(r + dr, c + dc, color, region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0 and grid[r, c] != 6:
                color = grid[r, c]
                region = []
                dfs(r, c, color, region)
                if region:  # Ensure region is not empty
                    regions.append(region)
        # After each row, reset visited for the next row to allow for vertically separated regions
        visited[r, :] = False

    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing white (0) and magenta (6) pixels and stacking the
    remaining colored regions, maintaining relative vertical order within each column.
    """
    input_grid = np.array(input_grid)
    regions = identify_regions(input_grid)

    # Create an empty output grid (initially same size as input)
    output_grid = np.zeros_like(input_grid)

    # Build column-wise stacks
    column_stacks = [[] for _ in range(input_grid.shape[1])]

    for region in regions:
        color = input_grid[region[0][0], region[0][1]]
        min_col = min(c for _, c in region)
        max_col = max(c for _, c in region)
        min_row = min(r for r,_ in region)

        # Add region to each relevant column stack
        for c in range(min_col, max_col + 1):
          for r,c2 in region:
            if c2 == c:
              column_stacks[c].append((r,color)) #append original row and color

    # Construct output grid from column stacks
    for c, stack in enumerate(column_stacks):
        #sort each stack by original row
        stack.sort()
        row_index = 0
        for r, color in stack:
            output_grid[row_index, c] = color
            row_index += 1

    return output_grid.tolist()