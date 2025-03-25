"""
The transformation rule identifies rectangular regions of the same color and
inserts an azure (color 8) rectangle in the empty space between them. The
inserted rectangle's dimensions and position are determined by the spatial
relationship between the existing rectangles, essentially filling the gap
between their projected boundaries.
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

def project_lines(rect1, rect2, rows, cols):
    """Projects lines from the edges of two rectangles."""

    min_r1, max_r1, min_c1, max_c1 = rect1
    min_r2, max_r2, min_c2, max_c2 = rect2
    
    # horizontal lines
    horiz_lines1 = [(min_r1,min_c1, min_r1, cols-1), (max_r1, min_c1, max_r1, cols-1)]
    horiz_lines2 = [(min_r2,min_c2, min_r2, cols-1), (max_r2, min_c2, max_r2, cols-1)]

    # vertical lines
    vert_lines1 = [(min_r1, min_c1, rows-1, min_c1), (min_r1, max_c1, rows -1, max_c1)]
    vert_lines2 = [(min_r2, min_c2, rows-1, min_c2), (min_r2, max_c2, rows -1, max_c2)]

    return horiz_lines1, horiz_lines2, vert_lines1, vert_lines2

def get_intersection(rect1, rect2, rows, cols):

    min_r1, max_r1, min_c1, max_c1 = rect1
    min_r2, max_r2, min_c2, max_c2 = rect2

    h1, h2, v1, v2 = project_lines(rect1, rect2, rows, cols)
    
    # Find intersection ranges
    r_start = max(min_r1, min_r2)
    r_end = min(max_r1, max_r2)
    c_start = max(min_c1, min_c2)
    c_end = min(max_c1, max_c2)

    # check for projections that would intersect without obstruction
    if min_r1 < min_r2 and max_r1 < max_r2:
        r_start = max_r1 + 1
        r_end = min_r2 - 1
    elif min_r2 < min_r1 and max_r2 < max_r1:
        r_start = max_r2 + 1
        r_end = min_r1 -1
    
    if min_c1 < min_c2 and max_c1 < max_c2:
        c_start = max_c1 + 1
        c_end = min_c2 - 1
    elif min_c2 < min_c1 and max_c2 < max_c1:
        c_start = max_c2 + 1
        c_end = min_c1 - 1


    if r_start <= r_end and c_start <= c_end:  # Use <= for inclusive range
            return (r_start, r_end, c_start, c_end)
    return None


def transform(input_grid):
    """
    Identifies rectangular regions of the same color and inserts an azure
    (color 8) rectangle in the space between their projected boundaries.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    rectangles = find_rectangles(grid)

    # Iterate through all pairs of rectangles of the same color
    for color, rects in rectangles.items():
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                intersection = get_intersection(rects[i], rects[j], rows, cols)
                if intersection:
                    r_start, r_end, c_start, c_end = intersection
                    # Fill the intersection with azure (color 8)
                    for r in range(r_start, r_end + 1):
                        for c in range(c_start, c_end + 1):
                            output_grid[r, c] = 8

    return output_grid.tolist()