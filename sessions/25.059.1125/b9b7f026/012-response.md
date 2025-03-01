# b9b7f026 • 012 • example_3 • investigate_coder

---
```python
"""
Counts the number of rectangles in the input grid that contain a "hole" (an inner region of a different color).
"""

import numpy as np

def find_rectangles(grid):
    """
    Finds all rectangles of uniform color in a grid.
    Returns a list of tuples, where each tuple represents a rectangle:
    ((row_start, col_start), (row_end, col_end), color)
    """
    rectangles = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, start_r, start_c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return

        visited[r, c] = True
        
        # Check neighbors
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            dfs(nr, nc, color, start_r, start_c)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    start_r, start_c = r, c
                    
                    # perform a depth first search to size the rectangle                    
                    dfs(r, c, color, start_r, start_c)
                    
                    # find bounding box 
                    min_r, max_r = rows, -1
                    min_c, max_c = cols, -1
                    
                    for rr in range(rows):
                        for cc in range(cols):
                            if visited[rr,cc] == True and grid[rr,cc] == color:
                                min_r = min(min_r, rr)
                                max_r = max(max_r, rr)
                                min_c = min(min_c, cc)
                                max_c = max(max_c, cc)
                    
                    rectangles.append(((min_r, min_c), (max_r, max_c), color))

    return rectangles

def has_hole(grid, rectangle):
    """
    Checks if a rectangle contains a "hole" (an inner region of a different color).
    """
    (r_start, c_start), (r_end, c_end), color = rectangle
    for r in range(r_start + 1, r_end):
        for c in range(c_start + 1, c_end):
            if grid[r, c] != color:
                return True
    return False

def transform(input_grid):
    # Find all rectangles in the input grid
    rectangles = find_rectangles(np.array(input_grid))

    # Count the number of rectangles with holes
    count = 0
    for rect in rectangles:
        if has_hole(np.array(input_grid), rect):
            count += 1

    # Output the count as a 1x1 grid
    output_grid = np.array([[count]])
    return output_grid
```
