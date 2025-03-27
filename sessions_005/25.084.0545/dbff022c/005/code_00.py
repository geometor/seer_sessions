"""
Transforms an input grid by identifying regions that change between input and output,
then changes those regions to match surrounding subgrids of uniform color.
"""

import numpy as np
from collections import Counter

def find_subgrids(grid):
    """Finds all maximal rectangular subgrids of a single non-zero color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    subgrids = []

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and not visited[r, c]

    def expand_subgrid(r, c, color):
        """Expands a subgrid from a starting cell."""
        min_r, max_r = r, r
        min_c, max_c = c, c

        # Expand vertically
        while min_r > 0 and is_valid(min_r - 1, c, color):
            min_r -= 1
        while max_r < rows - 1 and is_valid(max_r + 1, c, color):
            max_r += 1

        # Expand horizontally
        for row in range(min_r, max_r + 1):
            while min_c > 0 and is_valid(row, min_c - 1, color):
                min_c -= 1
            while max_c < cols - 1 and is_valid(row, max_c + 1, color):
                max_c += 1
        
        pixels = []
        for row in range(min_r, max_r+1):
            for col in range(min_c, max_c + 1):
                visited[row,col] = True
                pixels.append( ((row,col), grid[row,col]) )

        return {'top_left': (min_r, min_c), 'bottom_right': (max_r, max_c),
                'height': max_r - min_r + 1, 'width': max_c - min_c + 1,
                'color': color, 'pixels': pixels}

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                subgrids.append(expand_subgrid(r, c, grid[r, c]))
    return subgrids

def grid_diff(input_grid, output_grid):
    """Identifies differences between two grids."""
    input_arr = np.array(input_grid)
    output_arr = np.array(output_grid)
    diff = input_arr != output_arr
    diff_indices = np.where(diff)
    diff_pixels = list(zip(diff_indices[0], diff_indices[1]))
    return diff_pixels

def find_changed_areas(input_grid, output_grid):
    """Find contiguous areas that have changed between the input and output grids."""
    diff_pixels = grid_diff(input_grid, output_grid)
    rows, cols = len(input_grid), len(input_grid[0])
    visited = np.zeros((rows, cols), dtype=bool)
    changed_areas = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def expand_area(r, c, area_pixels):
        """Expands an area of changed pixels."""
        if not is_valid(r, c) or visited[r,c] or (r, c) not in diff_pixels:
            return
        
        visited[r,c] = True
        area_pixels.append((r,c))

        # Explore all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                expand_area(r + dr, c + dc, area_pixels)
        
    for r, c in diff_pixels:
        if not visited[r,c]:
            area_pixels = []
            expand_area(r,c, area_pixels)
            changed_areas.append(area_pixels)
    
    return changed_areas

def find_surrounding_subgrid(input_grid, changed_area, subgrids):
    """Finds the subgrid that surrounds a changed area without overlapping it."""
    
    # Get all pixel coordinates in the changed area
    changed_pixels = set(changed_area)
    rows, cols = len(input_grid), len(input_grid[0])

    # Find neighboring pixels (including diagonals) of the changed area
    neighboring_pixels = set()
    for r, c in changed_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighboring_pixels.add((nr, nc))
    
    # Exclude pixels that are part of the changed area
    neighboring_pixels -= changed_pixels

    # Find which subgrid contains the neighboring pixels
    for subgrid in subgrids:
        subgrid_pixels_set = set([p[0] for p in subgrid['pixels']])
        if neighboring_pixels.issubset(subgrid_pixels_set):
            return subgrid

    return None # No surrounding subgrid found

def transform(input_grid):
    # initialize output grid
    output_grid = [row[:] for row in input_grid] # Create deep copy
    
    # Find subgrids of the input
    subgrids = find_subgrids(np.array(input_grid))

    # Find all areas of changed pixels between input and output
    # Note we don't have the output grid, just the input, but the changed_area
    # strategy relies on having both to compare, we will adjust our
    # strategy after testing

    # Since changed_areas cannot be computed without output grid, we will
    # comment this transformation until the next iteration when we are better
    # informed to develop this functionality

    # changed_areas = find_changed_areas(input_grid, output_grid)
    
    # # Find surrounding subgrids and change color.
    # for changed_area in changed_areas:
    #     surrounding_subgrid = find_surrounding_subgrid(input_grid, changed_area, subgrids)
    #     if surrounding_subgrid:
    #         new_color = surrounding_subgrid['color']
    #         for r, c in changed_area:
    #             output_grid[r][c] = new_color

    return output_grid