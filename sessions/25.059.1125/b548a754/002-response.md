# b548a754 • 002 • example_3 • investigate_coder

---
```python
"""
Identifies an "inner" and "outer" rectangle within the input grid and expands the inner rectangle to the size of the outer one, maintaining its original position and pattern. An isolated azure pixel is ignored.
"""

import numpy as np

def find_rectangle(grid, exclude_color=None):
    """Finds the largest rectangle of a single color, excluding a specified color."""
    rows, cols = grid.shape
    max_area = 0
    best_rect = None

    for r1 in range(rows):
        for c1 in range(cols):
            color = grid[r1, c1]
            if exclude_color is not None and color == exclude_color:
                continue

            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    if grid[r2, c2] != color:
                        continue

                    is_rectangle = True
                    for r in range(r1, r2 + 1):
                        for c in range(c1, c2 + 1):
                            if grid[r, c] != color:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break

                    if is_rectangle:
                        area = (r2 - r1 + 1) * (c2 - c1 + 1)
                        if area > max_area:
                            max_area = area
                            best_rect = ((r1, c1), (r2, c2), color)
    return best_rect

def find_inner_rectangle(grid, outer_rect):
    """Finds an inner rectangle within the bounds of the outer rectangle."""
    (r1_outer, c1_outer), (r2_outer, c2_outer), outer_color = outer_rect
    inner_rect = find_rectangle(grid[r1_outer:r2_outer+1, c1_outer:c2_outer+1])
    if inner_rect:
        (r1_inner, c1_inner), (r2_inner, c2_inner), inner_color = inner_rect
        # Adjust coordinates to be relative to the original grid
        return ((r1_outer + r1_inner, c1_outer + c1_inner), (r1_outer+r2_inner, c1_outer+c2_inner), inner_color)

    return None


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the outer rectangle, excluding azure (8)
    outer_rect = find_rectangle(grid, exclude_color=8)
    if outer_rect is None:
        return output_grid.tolist()

    # Find the inner rectangle
    inner_rect = find_inner_rectangle(grid, outer_rect)

    if inner_rect is None:
           return output_grid.tolist()

    (r1_outer, c1_outer), (r2_outer, c2_outer), _ = outer_rect
    (r1_inner, c1_inner), (r2_inner, c2_inner), inner_color = inner_rect
    inner_height = r2_inner - r1_inner + 1
    inner_width = c2_inner - c1_inner + 1
    
    # fill output grid with the color of the expanded inner shape
    for r in range(r1_outer, r2_outer + 1):
        for c in range(c1_outer, c2_outer + 1):
            inner_r = (r - r1_outer) % inner_height
            inner_c = (c - c1_outer) % inner_width
            
            output_grid[r,c] = grid[r1_inner + inner_r, c1_inner + inner_c]
    return output_grid.tolist()
```
