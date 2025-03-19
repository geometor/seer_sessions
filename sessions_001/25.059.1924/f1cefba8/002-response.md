# f1cefba8 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate the outer and inner rectangles based on their colors and contiguous shapes. The background consists of black pixels.
2.  **Process Inner Rectangle:**
    *   Identify the inner rectangle's color.
    *   Invert color of pixels in the edges of the inner rectangle (change green to red, blue to yellow, red to green, yellow to blue).
3.  **Add Background Elements:**
    *   Extend vertical and horizontal lines from the inner rectangle's edges, crossing the entire grid, inverting colors of every inner rectangle's pixel on the edges.
4. **Modify Background**
    *   Change original background pixels (originally black) to the inverted colors of the elements added in the previous step, according to the lines position.
"""

import numpy as np

def find_rectangle(grid, color=None):
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if (color is None and grid[r,c] != 0) or (color is not None and grid[r,c] == color):
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1: # No rectangle found
        return None
    
    return (min_row, min_col, max_row, max_col)
    

def invert_color(color):
    inversion_map = {
        1: 4,  # blue to yellow
        4: 1,  # yellow to blue
        2: 3,  # red to green
        3: 2,  # green to red
        8: 8,  # azure stays same
        0: 0   # Black stays black
    }
    return inversion_map.get(color, color) # Return original if not found

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find the outer rectangle (any non-black color)
    outer_rect = find_rectangle(input_grid)
    if outer_rect is None:
        return output_grid # Early exit if not found.
    
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = outer_rect

    # Find Inner rectangle
    inner_rect_colors = []
    for r in range(outer_min_row + 1, outer_max_row):
        for c in range(outer_min_col + 1, outer_max_col):
            if input_grid[r,c] != input_grid[outer_min_row, outer_min_col] and input_grid[r,c] != 0:
               inner_rect_colors.append(input_grid[r,c])
    
    inner_rect_colors = list(set(inner_rect_colors))
    
    if len(inner_rect_colors) > 0:
        inner_rect = find_rectangle(input_grid,inner_rect_colors[0])
    else: # There is no inner rectangle
       return output_grid 

    if inner_rect is None:
        return output_grid
    
    inner_min_row, inner_min_col, inner_max_row, inner_max_col = inner_rect

    # Invert inner rectangle edges colors
    for c in range(inner_min_col, inner_max_col + 1):
        output_grid[inner_min_row, c] = invert_color(input_grid[inner_min_row, c]) # Top
        output_grid[inner_max_row, c] = invert_color(input_grid[inner_max_row, c]) # Bottom
        
    for r in range(inner_min_row, inner_max_row + 1):
        output_grid[r, inner_min_col] = invert_color(input_grid[r, inner_min_col])  # Left
        output_grid[r, inner_max_col] = invert_color(input_grid[r, inner_max_col])  # Right

    # Add background cross
    
    # Horizontal
    for c in range(0, cols):
        if c < inner_min_col or c > inner_max_col:
            if input_grid[inner_min_row, inner_min_col] != 0:
               output_grid[inner_min_row,c] = invert_color(input_grid[inner_min_row, inner_min_col])
            if input_grid[inner_max_row, inner_min_col] != 0:
               output_grid[inner_max_row,c] = invert_color(input_grid[inner_max_row, inner_min_col])
        
    # Vertical
    for r in range(0, rows):
        if r < inner_min_row or r > inner_max_row:
            if input_grid[inner_min_row, inner_min_col] != 0:
                output_grid[r,inner_min_col] = invert_color(input_grid[inner_min_row, inner_min_col])
            if input_grid[inner_min_row, inner_max_col] != 0:
                output_grid[r,inner_max_col] = invert_color(input_grid[inner_min_row, inner_max_col])

    return output_grid
```
