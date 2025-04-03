```python
import numpy as np
from collections import deque

"""
Identifies connected regions of non-zero colors in the input grid. 
If any part of a region touches the outer border of the grid, the entire region is removed (set to 0). 
Regions entirely contained within the grid (not touching any border) are preserved in the output.
"""

def _find_regions(grid):
    """
    Finds all connected regions of non-zero cells using BFS.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'color', 'cells' (a set of (row, col) tuples),
              and 'touches_border' (boolean).
    """
    rows, cols = grid.shape
    visited = set()
    regions = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not yet visited, start a BFS
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                current_region_cells = set()
                touches_border = False
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_region_cells.add((row, col))

                    # Check if the current cell is on the border
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        touches_border = True

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if not visited, and if it's part of the same color region
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                regions.append({
                    'color': color,
                    'cells': current_region_cells,
                    'touches_border': touches_border
                })
    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing connected regions of non-zero colors
    if they touch the grid border.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Initialize output_grid with zeros (background color)
    output_grid = np.zeros_like(grid_np)

    # Find all regions in the input grid
    regions = _find_regions(grid_np)

    # Iterate through the found regions
    for region in regions:
        # If a region does NOT touch the border, copy it to the output grid
        if not region['touches_border']:
            color = region['color']
            for r, c in region['cells']:
                output_grid[r, c] = color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```