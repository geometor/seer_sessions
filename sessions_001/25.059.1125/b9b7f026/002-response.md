# b9b7f026 • 002 • example_3 • investigate_coder

---
```python
"""
1. Identify Rectangles: Examine the input grid and identify all distinct rectangular shapes formed by contiguous pixels of the same color.
2. Find "Inside" Rectangle: If a rectangle fully encloses the non-zero pixels of one and only one other rectangle, select the inside rectangle.
3. Output Color: Output the color code (single digit integer) of that inside rectangle.
"""

import numpy as np

def find_rectangles(grid):
    """Finds all rectangles in a grid."""
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
            if grid[r, c] != 0 and (r, c) not in visited:
                coords = []
                dfs(r, c, grid[r, c], coords)
                if coords:
                    min_r = min(cr[0] for cr in coords)
                    max_r = max(cr[0] for cr in coords)
                    min_c = min(cr[1] for cr in coords)
                    max_c = max(cr[1] for cr in coords)
                    # Store rectangle as (color, (min_r, min_c, max_r, max_c))
                    rectangles[(min_r, min_c, max_r, max_c)] = grid[r,c]
    return rectangles

def find_inner_rectangle(rectangles):
    """Finds the inner rectangle enclosed by exactly one other rectangle."""
    
    for rect1_coords, color1 in rectangles.items():
        enclosing_count = 0
        inner_rect = None
        for rect2_coords, color2 in rectangles.items():
            if rect1_coords != rect2_coords:  # Don't compare a rectangle to itself
                # Check if rect2 encloses rect1.
                if (rect2_coords[0] < rect1_coords[0] and  # top
                    rect2_coords[1] < rect1_coords[1] and  # left
                    rect2_coords[2] > rect1_coords[2] and  # bottom
                    rect2_coords[3] > rect1_coords[3]):     # right
                  
                    #Check that rect1 only encloses non-zero pixels of rect 2
                    all_contained = True
                    for r in range(rect1_coords[0], rect1_coords[2] + 1):
                        for c in range(rect1_coords[1], rect1_coords[3] + 1):
                            if (r,c) not in [(r,c) for r in range(rect2_coords[0],rect2_coords[2]+1) for c in range(rect2_coords[1],rect2_coords[3]+1)]:
                                if (r,c) in [(coord[0], coord[1]) for coordList in [list(zip(*([(rr, cc) for rr in range(r1, r2 + 1) for cc in range(c1, c2 + 1)]))) for (r1, c1, r2, c2), _ in rectangles.items()] :
                                    all_contained = False
                                    break
                        if not all_contained:
                            break
                    if all_contained:
                        enclosing_count += 1
                        inner_rect = rect2_coords

        if enclosing_count == 1:
            return rectangles[inner_rect]  # Return the *color* of the inner rectangle

    return None  # No inner rectangle found based on criteria


def transform(input_grid):
    """Transforms the input grid to the output grid."""
    # Find all rectangles
    rectangles = find_rectangles(np.array(input_grid))

    # Find the inner rectangle
    inner_color = find_inner_rectangle(rectangles)

    # Output the color of the inner rectangle
    if inner_color is not None:
        return inner_color
    else:
        return 0
```
