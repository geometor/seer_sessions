"""
1. Expand White Edge: Find all white (0) pixels on the edge of the grid and change them to green (3).
2. Identify Maroon Objects: Locate all objects (contiguous regions) of color 9 (maroon) in the input grid.
3. Expand Maroon Objects: Expand each maroon object by one layer, adding a green (3) outline to any adjacent white (0) pixels.
4. Flood Fill Enclosed Area: Find any area completely enclosed by green (3) and flood fill that area with blue (1).
"""

import numpy as np

def expand_white_edge(grid):
    # Expand white cells adjacent to any edge and convert them to green
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0:
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    output_grid[r, c] = 3
    return output_grid

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                objects.append(dfs(r, c))
    return objects

def expand_region(grid, region, expansion_color):
    # Expand the region by one layer, adding an outline on white pixels with expansion color
    expanded_region = set(region)
    output_grid = np.copy(grid)

    for r, c in region:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and
                    grid[nr, nc] == 0):
                expanded_region.add((nr, nc))
                output_grid[nr, nc] = expansion_color
    return list(expanded_region), output_grid

def flood_fill(grid, start_row, start_col, fill_color):
    """Fills a bounded region with the specified color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    stack = [(start_row, start_col)]
    original_color = grid[start_row, start_col]
    
    if original_color == fill_color:
        return grid

    output_grid = np.copy(grid)

    while stack:
        r, c = stack.pop()
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or output_grid[r,c] != original_color:
            continue
        
        visited[r, c] = True
        output_grid[r,c] = fill_color
        
        stack.append((r + 1, c))
        stack.append((r - 1, c))
        stack.append((r, c + 1))
        stack.append((r, c - 1))
    return output_grid
    
def find_enclosed_area_and_fill(grid, boundary_color, fill_color):
    rows, cols = grid.shape
    output_grid = np.copy(grid)

    def is_enclosed(r, c, visited):
      # check if the cell can reach edge
        if (r <= 0 or r >= rows - 1 or c <= 0 or c >= cols - 1):
            return False

        visited.add((r,c))
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        for nr, nc in neighbors:
            if (nr, nc) not in visited:
                if output_grid[nr, nc] != boundary_color:
                    if not is_enclosed(nr, nc, visited):
                       return False

        return True


    for r in range(1, rows-1):
        for c in range(1, cols-1):
            if grid[r,c] != boundary_color and grid[r,c] != fill_color:
                visited = set()
                if is_enclosed(r, c, visited):
                   output_grid = flood_fill(output_grid, r, c, fill_color)

    return output_grid

def transform(input_grid):
    # 1. Expand White Edge
    output_grid = expand_white_edge(input_grid)

    # 2. Identify Maroon Regions
    maroon_regions = find_objects(output_grid, 9)  # Find maroon objects *after* edge expansion

    # 3. Expand Maroon Regions
    for region in maroon_regions:
        _, output_grid = expand_region(output_grid, region, 3) # Expand using the modified grid

    # 4. Flood fill enclosed area
    output_grid = find_enclosed_area_and_fill(output_grid, 3, 1)

    return output_grid