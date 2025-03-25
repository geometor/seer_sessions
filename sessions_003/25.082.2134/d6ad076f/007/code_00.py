"""
The transformation rule identifies rectangular regions of the same color and
inserts an azure (color 8) rectangle in the empty space between them. The
inserted rectangle's dimensions and position are determined by the spatial
relationship between the existing rectangles, essentially filling the maximal
empty gap between their closest edges.
"""

import numpy as np

def find_rectangles(grid):
    """Finds all distinct, non-overlapping rectangles of the same color."""
    rectangles = {}
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                coords = []
                dfs(r, c, color, coords)
                if coords:
                    min_r = min(cr for cr, _ in coords)
                    max_r = max(cr for cr, _ in coords)
                    min_c = min(cc for _, cc in coords)
                    max_c = max(cc for _, cc in coords)
                    
                    # check if it is a rectangle
                    is_rectangle = True
                    for cr in range(min_r, max_r + 1):
                        for cc in range(min_c, max_c + 1):
                            if grid[cr,cc] != color:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break
                    if is_rectangle:
                        rectangles.setdefault(color, []).append((min_r, max_r, min_c, max_c))
    return rectangles

def find_empty_regions(grid):
    """Finds connected regions of background color (0)."""
    empty_regions = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != 0:
            return
        visited.add((r, c))
        coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] == 0:
                coords = []
                dfs(r, c, coords)
                if coords:
                    min_r = min(cr for cr, _ in coords)
                    max_r = max(cr for cr, _ in coords)
                    min_c = min(cc for _, cc in coords)
                    max_c = max(cc for _, cc in coords)
                    empty_regions.append((min_r, max_r, min_c, max_c, coords))
    return empty_regions

def is_inbetween(empty_region, rectangles):
    """
    Checks if an empty region is "in-between" at least two different colored rectangles.
    """
    min_r, max_r, min_c, max_c, coords = empty_region
    adjacent_colors = set()
    
    for r, c in coords:
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            nr, nc = r + dr, c + dc
            for color, rects in rectangles.items():
                 for rect in rects:
                    rect_min_r, rect_max_r, rect_min_c, rect_max_c = rect
                    if rect_min_r <= nr <= rect_max_r and rect_min_c <= nc <= rect_max_c:
                       adjacent_colors.add(color)

    return len(adjacent_colors) >= 2

def transform(input_grid):
    """
    Identifies rectangular regions of the same color and inserts an azure
    (color 8) rectangle in the space between their projected boundaries.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rectangles = find_rectangles(grid)
    empty_regions = find_empty_regions(grid)

    # Iterate through all empty regions
    for empty_region in empty_regions:
        if is_inbetween(empty_region, rectangles):
            min_r, max_r, min_c, max_c, coords = empty_region
            # Fill the inbetween region with azure (color 8)
             for r, c in coords:
                output_grid[r,c] = 8

    return output_grid.tolist()