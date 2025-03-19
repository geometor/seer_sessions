# 264363fd • 012 • refine_coder

---
```python
"""
1.  **Identify and Remove:** Locate and remove all blue pixels, these constitute the background.

2.  **Identify and Remove:** Locate all single yellow pixels (1x1 yellow rectangles) and remove them.

3.  **Identify and Shift Rectangles:** Find all red rectangles. Shift each red rectangle to the leftmost position within its row. Maintain the rectangle's shape during the shift.

4.  **Identify Green Lines:** Find the original positions of green pixels. For each row or column that contains green pixels, perform the next step.

5.  **Alternate Line Colors:** Starting with red, alternate the colors between red and green *only* at the original positions where a green pixel was found, skip the other positions.
"""

import numpy as np

def find_rectangles(grid, color):
    rectangles = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_rectangle):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_rectangle.append((r, c))
        dfs(r + 1, c, current_rectangle)
        dfs(r - 1, c, current_rectangle)
        dfs(r, c + 1, current_rectangle)
        dfs(r, c - 1, current_rectangle)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_rectangle = []
                dfs(r, c, current_rectangle)
                if len(current_rectangle) > 1: # Only consider rectangles (not 1x1 pixels)
                    rectangles.append(current_rectangle)
    return rectangles

def shift_rectangle_left(grid, rectangle):
    min_col = min(c for r, c in rectangle)
    for r, c in rectangle:
        grid[r, c - min_col] = grid[r,c] #fill new spot
        if (c-min_col) != c:
            grid[r, c] = 0 #erase old by setting to background
    return grid

def find_green_positions(grid):
    positions = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 3:
                positions.append((r,c))
    return positions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Remove blue background
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 1:
                output_grid[r, c] = 0

    # Find red rectangles (this also excludes 1x1 yellow pixels).
    red_rectangles = find_rectangles(output_grid, 2)

    # Shift rectangles left.
    for rectangle in red_rectangles:
        output_grid = shift_rectangle_left(output_grid, rectangle)

    #Find green positions
    green_positions = find_green_positions(input_grid) #use input_grid

    #Alternate colors in lines
    for r, c in green_positions:
        output_grid[r,c] = 2 if (green_positions.index((r,c)) % 2 == 0) else 3 # alternate based on position in list

    return output_grid
```
