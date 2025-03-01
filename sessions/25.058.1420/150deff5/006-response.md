# 150deff5 • 006 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Identify the Object:** Find the contiguous block of pixels with color 5 (gray) in the input grid.
2.  **Outline the Object:** Replace the outer boundary pixels of the gray object with color 8 (azure).
3.  **Process Inner Pixels by Rows:** For the remaining (inner) pixels:
    *   Group them by their row.
    *   Within each row, sort the inner pixels by their column index.
    *   Process each row group:
        * find the 'center' pixels. If odd length, one center. If even, two centers.
        * set center pixel(s) to 8 (azure)
        * set the remaining pixels to 2 (red)

"""

import numpy as np

def get_object(grid, color):
    """
    Finds the coordinates of a contiguous object of a specified color.
    """
    object_coords = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                dfs(r, c)
                return object_coords  # Return after finding the first object
    return []


def get_outer_pixels(grid, object_coords):
    """
    Determines the outer boundary pixels of an object.
    """
    
    rows, cols = grid.shape
    outer_pixels = set()
    for r,c in object_coords:
        for dr, dc in [(0,1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols and (nr, nc) in object_coords):
                outer_pixels.add((r,c))
                break # move onto next pixel
    return list(outer_pixels)
    

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify the Object
    object_coords = get_object(input_grid, 5)
    if not object_coords:
        return output_grid.tolist()

    # 2. Outer Replacement
    outer_pixels = get_outer_pixels(input_grid, object_coords)
    for r, c in outer_pixels:
        output_grid[r, c] = 8

    # 3. Inner Replacement
    inner_pixels_set = set(object_coords) - set(outer_pixels)
    inner_pixels = list(inner_pixels_set)

    # Group by rows
    rows_dict = {}
    for r, c in inner_pixels:
        if r not in rows_dict:
            rows_dict[r] = []
        rows_dict[r].append((r, c))
    
    # process lines in each row
    for r in rows_dict:
        row_coords = sorted(rows_dict[r], key=lambda x:x[1]) #sort by column
        line_length = len(row_coords)
        
        if line_length > 0:
          if line_length % 2 == 1: # odd
            mid = line_length // 2
            output_grid[row_coords[mid]] = 8
            for i in range(line_length):
                if i != mid:
                  output_grid[row_coords[i]] = 2
          else: # even
            mid1 = line_length // 2 - 1
            mid2 = line_length // 2
            output_grid[row_coords[mid1]] = 8
            output_grid[row_coords[mid2]] = 8
            for i in range(line_length):
                if i != mid1 and i != mid2:
                  output_grid[row_coords[i]] = 2
    

    return output_grid.tolist()
```
