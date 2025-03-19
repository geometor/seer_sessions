# f8b3ba0a • 012 • refine_coder

---
```python
"""
1. **Identify Colored Regions:** Examine the input grid and identify all contiguous regions of the same color (excluding the background color 0).
2.  **Select Columnar Colors**. Select the colors that appear in a single vertical column within the input.
3. **Order colors:** Preserve the vertical order in the input.
4.  **Output:** Create a vertical Nx1 grid, where N is the number of selected, ordered colors. List the selected colors in individual cells.
"""

import numpy as np

def get_colored_regions(grid):
    """
    Identifies contiguous regions of the same color (excluding 0) in the grid.
    Returns a dictionary of colors and coordinates.
    """
    visited = set()
    regions = {}

    rows, cols = grid.shape

    def _explore_region(row, col, color, current_region):
      if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
        return
      
      visited.add((row, col))
      current_region.append( (row, col) )
      
      _explore_region(row+1, col, color, current_region) # down
      _explore_region(row-1, col, color, current_region) # up
      _explore_region(row, col+1, color, current_region) # right
      _explore_region(row, col-1, color, current_region) # left

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                current_region = []
                _explore_region(r, c, color, current_region)
                if color not in regions:
                  regions[color] = []
                regions[color].append(current_region)

    return regions

def get_columnar_colors(grid):
    """Selects colors that form a single vertical column."""
    rows, cols = grid.shape
    for col in range(cols):
        column_colors = []
        for row in range(rows):
            color = grid[row, col]
            if color != 0:
                column_colors.append(color)
        if column_colors: # only uses first non-empty column
            return column_colors
    return []


def transform(input_grid):
    """Transforms the input grid to output a vertical grid of unique colors.
    """
    # Find colored regions (not strictly needed, but kept for potential future use)
    # regions = get_colored_regions(input_grid) # keeping in case future need

    # Get the order of colors from a single vertical column
    ordered_colors = get_columnar_colors(input_grid)

    # Create output grid
    output_grid = np.array(ordered_colors).reshape(-1, 1)

    return output_grid
```
