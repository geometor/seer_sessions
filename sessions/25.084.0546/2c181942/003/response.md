```python
"""
1.  **Identify Regions:** Find all contiguous colored regions (non-azure pixels) in the input grid. Each region is defined by the (row, column) coordinates of its pixels and its color.

2.  **Check for Empty Rows:** If a region's topmost row contains *only* azure pixels, the region does not change and is kept in the final output.

3.  **Vertical Alignment and Combination**: For regions *not* handled in step 2, examine their vertical relationships with other regions:
    - find regions that have at least one column in common with each other (vertically aligned, not necessarily adjacent).
    - combine the vertically aligned regions into one by stacking them in the output from top to bottom based on color:
      - The resulting combined region should be placed starting at the top-most row possible.

4. **Output:** Generate the output grid by keeping the original regions from step 2 and by placing the shifted/combined regions from step 3. The azure background remains unchanged.
"""

import numpy as np

def get_colored_regions(grid):
    """
    Identifies and returns a list of colored regions (non-azure pixels).
    Each region is a list of (row, col) tuples.
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
                regions.append((current_region, grid[row,col])) # Store color with region
    return regions

def is_row_empty(grid, row, exclude_color=8):
    """Checks if a given row contains only the exclude_color."""
    for cell in grid[row]:
        if cell != exclude_color:
            return False
    return True

def find_vertically_aligned_regions(regions):
    """
    Finds and returns a list of vertically aligned regions.
    Regions are vertically aligned if they share at least one column index.
    """
    aligned_groups = []
    for i in range(len(regions)):
        region1, color1 = regions[i]
        group = [regions[i]]
        for j in range(i + 1, len(regions)):
            region2, color2 = regions[j]
            cols1 = set([col for row, col in region1])
            cols2 = set([col for row, col in region2])
            if len(cols1.intersection(cols2)) > 0:
                group.append(regions[j])
        if len(group) > 1:
          aligned_groups.append(group)
    return aligned_groups

def combine_regions(region_group, rows):
    """
    Combines vertically aligned regions by stacking them.
    """
    combined_pixels = []
    current_row = 0
    sorted_regions = sorted(region_group, key=lambda x: x[1]) # sort by color

    for region, color in sorted_regions: # region is the list of coordinates
      region_height = max(r for r, _ in region) - min(r for r, _ in region) + 1
      for row, col in region:
          new_row = row - min(r for r, _ in region) + current_row
          combined_pixels.append((new_row,col,color))
      current_row += region_height
      #current_row = min(rows, current_row)  # Prevent exceeding grid bounds - this caused a bug

    return combined_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    grid = np.array(input_grid)
    output_grid = np.full(grid.shape, 8, dtype=int) # init with azure
    rows, cols = grid.shape

    # 1. Identify colored regions
    regions = get_colored_regions(grid)

    # 2. Handle regions on empty rows
    for region, color in regions:
        first_row = region[0][0]
        if is_row_empty(grid, first_row):
            for row, col in region:
                output_grid[row, col] = color

    # 3. Vertical Alignment and Combination
    aligned_groups = find_vertically_aligned_regions(regions)


    for group in aligned_groups:
      # check that regions in group are *not* all in empty rows
      all_empty = True
      for region, _ in group:
        first_row = region[0][0]
        if not is_row_empty(grid, first_row):
          all_empty = False
          break

      if not all_empty:
        combined = combine_regions(group, rows)
        for row, col, color in combined:
          if row < rows: # check to prevent out of bounds
            output_grid[row, col] = color

    return output_grid.tolist()
```