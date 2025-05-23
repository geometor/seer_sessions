"""
Identifies green areas in the input grid, and changes the color of a specific pixel within that area to yellow. The target pixel prioritizes "center" pixels (not touching non-green or boundary) but if none exist, it uses these priorities (rightmost, then down, then leftmost).
"""

import numpy as np

def find_green_areas(grid):
    """Finds all connected green areas in the grid."""
    green_pixels = np.argwhere(grid == 3)
    if len(green_pixels) == 0:
        return []

    areas = []
    visited = set()

    def _dfs(r, c, current_area):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != 3:
            return
        visited.add((r, c))
        current_area.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(r + dr, c + dc, current_area)

    for r, c in green_pixels:
        if (r, c) not in visited:
            current_area = []
            _dfs(r, c, current_area)
            areas.append(current_area)

    return areas

def find_target_pixel(grid, area):
    """Finds the target pixel within a green area."""
    rows, cols = grid.shape

    # Check for center pixels
    for r, c in area:
        is_center = True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 3):
                is_center = False
                break
        if is_center:
            return (r, c)

    # If no center pixel, select based on priority (right, down, left)
    if not area:  # Handle empty area case
      return None

    # Sort by column (descending), then row (descending), then column (ascending)
    sorted_area = sorted(area, key=lambda p: (-p[1], -p[0], p[1]))
    return sorted_area[0]
    

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all green areas
    green_areas = find_green_areas(input_grid)

    # If no green areas, return the original grid
    if not green_areas:
        return output_grid

    # Select the first green area (based on the analysis, any area can be selected)
    target_area = green_areas[0]


    # Find the target pixel within the largest area
    target_pixel = find_target_pixel(output_grid, target_area)

    # Change the color of the target pixel to yellow (4)
    if target_pixel:
        output_grid[target_pixel] = 4

    return output_grid