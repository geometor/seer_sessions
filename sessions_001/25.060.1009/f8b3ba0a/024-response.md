# f8b3ba0a • 024 • refine_coder

---
```python
"""
1.  **Identify Rectangles:** Scan the input grid to locate all rectangular regions of uniform color.  The rectangle must be at least 2 pixels in either width or height.
2.  **Extract Color:** For each rectangular region found, extract its color.
3.  **Output List:** Create a list containing the extracted colors, removing duplicates.
"""

import numpy as np

def find_rectangles(grid):
    """Finds all rectangular regions of uniform color with min size 2 in any dimension."""
    height, width = grid.shape
    rectangles = []
    visited = np.zeros((height, width), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < height and 0 <= c < width

    def dfs(r, c, color, current_rectangle):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_rectangle.append((r, c))
        
        dfs(r + 1, c, color, current_rectangle)
        dfs(r - 1, c, color, current_rectangle)
        dfs(r, c + 1, color, current_rectangle)
        dfs(r, c - 1, color, current_rectangle)

    for r in range(height):
        for c in range(width):
            if not visited[r, c] and grid[r,c] != 0:
                current_rectangle = []
                dfs(r, c, grid[r, c], current_rectangle)
                if current_rectangle:
                    # Check if it's a rectangle
                    rows, cols = zip(*current_rectangle)
                    min_row, max_row = min(rows), max(rows)
                    min_col, max_col = min(cols), max(cols)
                    
                    if (max_row - min_row + 1) * (max_col - min_col + 1) == len(current_rectangle) and (max_row - min_row +1 >= 2 or max_col-min_col + 1 >= 2):
                         rectangles.append((grid[r, c], current_rectangle))


    return rectangles

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)

    # Find rectangles
    rectangles = find_rectangles(grid)

    # Extract colors
    extracted_colors = [color for color, _ in rectangles]
    
    # remove duplicates
    output_list_no_duplicates = []
    for color in extracted_colors:
        if color not in output_list_no_duplicates:
            output_list_no_duplicates.append(color)


    return output_list_no_duplicates
```
