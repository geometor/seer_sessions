"""
Identifies green areas in the input grid, selects the largest one if multiple exist, and changes the color of a specific pixel within that area to yellow. The target pixel prioritizes "center" pixels (not touching non-green or boundary) but defaults to the top-leftmost green pixel if all are on the edge.
"""

import numpy as np

def find_green_areas(grid):
    # Find all green pixels
    green_pixels = np.argwhere(grid == 3)
    
    # If no green pixels, return empty list
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

def select_largest_area(areas):
    if not areas:
        return []
    return max(areas, key=len)

def find_target_pixel(grid, area):
    # Try to find a "center" pixel first
    rows, cols = grid.shape
    for r, c in area:
        is_center = True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] != 3:
                    is_center = False
                    break
            else:
                is_center = False  # Boundary touch
                break
        if is_center:
            return (r, c)

    # If no center pixel, return top-leftmost
    return min(area, key=lambda p: (p[0], p[1]))

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all green areas
    green_areas = find_green_areas(input_grid)

    # If no green areas, return the original grid
    if not green_areas:
        return output_grid

    # Select the largest green area
    largest_area = select_largest_area(green_areas)

    # Find the target pixel within the largest area
    target_pixel = find_target_pixel(input_grid, largest_area)
    
    # Change the color of the target pixel to yellow (4)
    if target_pixel:
      output_grid[target_pixel] = 4

    return output_grid