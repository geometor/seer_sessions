"""
1.  **Identify Regions:** Find all contiguous regions of non-azure pixels in the input grid. Each region is defined by a list of `(row, column)` coordinates and its color.

2.  **Check for Top Empty Rows:** For each region, determine if its topmost row in the *original* input grid consisted *only* of azure pixels.

3.  **Stack Regions:** Stack the regions in the output grid. The regions will retain their original shapes.
    *   Regions should appear from top to bottom, based on the order of their topmost row in the input grid. Regions with lower row numbers are stacked higher.
    *   Regions where the top row was all azure in the *original* input grid should *not* be moved; they remain in their original positions.
    *   Regions will stack starting at the top and moving down

4.  **Output:** Create the output grid with azure as the background. Place the regions according to the stacking rules, overriding the background color where regions are placed.
"""

import numpy as np

def get_colored_regions(grid):
    """
    Identifies and returns a list of colored regions (non-azure pixels).
    Each region is a tuple: (list of (row, col) tuples, color).
    """
    regions = []
    visited = set()
    rows, cols = grid.shape

    def _dfs(row, col, current_region, color):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(row + dr, col + dc, current_region, color)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 8 and (row, col) not in visited:
                current_region = []
                _dfs(row, col, current_region, grid[row, col])
                regions.append((current_region, grid[row, col]))  # Store color with region
    return regions

def is_top_row_empty(grid, region_coords):
    """Checks if the topmost row of a region contains only azure pixels."""
    top_row = min(r for r, _ in region_coords)
    for col in range(grid.shape[1]):
        if (top_row, col) in region_coords: # important to check if in region
          if grid[top_row,col] != 8:
              return False
    return True

def stack_regions(regions, grid_shape, input_grid):
    """Stacks regions, preserving shape, based on original vertical order."""
    output_grid = np.full(grid_shape, 8, dtype=int)  # Initialize with azure
    current_row = 0

    # Sort regions by their topmost row in the original grid
    sorted_regions = sorted(regions, key=lambda item: min(row for row, _ in item[0]))

    for region_coords, color in sorted_regions:
        top_row = min(r for r, _ in region_coords)
        region_height = max(r for r, _ in region_coords) - top_row + 1

        if not is_top_row_empty(input_grid, region_coords):
            # Calculate the row offset for stacking
            row_offset = current_row - top_row

            # Place the region in the output grid
            for row, col in region_coords:
                new_row = row + row_offset
                if 0 <= new_row < grid_shape[0]: # boundary check
                  output_grid[new_row, col] = color

            current_row += region_height  # Update current_row for the next region
        else:
          # Keep in original position
          for row, col in region_coords:
            output_grid[row,col] = color
    return output_grid

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # 1. Identify colored regions
    regions = get_colored_regions(grid)

    # 2 & 3. Stack regions, handling the top-empty condition
    output_grid = stack_regions(regions, grid.shape, grid)

    return output_grid.tolist()