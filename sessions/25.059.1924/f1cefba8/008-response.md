# f1cefba8 • 008 • refine_coder

---
```python
"""
The transformation identifies a region of red pixels enclosed by an azure border. It expands this region by adding a row above and below, filling the entire expanded region (excluding the azure border itself) with red, and finally adding red pixels to the four corners of the expanded azure border.
"""

import numpy as np

def find_enclosed_region(grid, border_color, inner_color):
    """Finds the coordinates of all inner_color pixels enclosed by border_color."""
    rows, cols = grid.shape
    enclosed_pixels = []
    visited = set()

    # Find a starting inner pixel
    start_pixel = None
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == inner_color:
                start_pixel = (r, c)
                break
        if start_pixel:
            break

    if not start_pixel:
        return []

    # Depth-first search to find all connected inner pixels
    stack = [start_pixel]
    while stack:
        r, c = stack.pop()
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r,c] == border_color:
            continue
        visited.add((r, c))
        
        if grid[r,c] == inner_color:
          enclosed_pixels.append((r,c))
          # Add neighbors to the stack
          stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

    return enclosed_pixels

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return None
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    azure_color = 8
    red_color = 2

    # 1. Find the enclosed red region
    enclosed_red_pixels = find_enclosed_region(input_grid, azure_color, red_color)

    # If no enclosed region is present return a copy
    if not enclosed_red_pixels:
        return output_grid

    # 2. Get the bounding box of the red region
    min_row, min_col, max_row, max_col = get_bounding_box(enclosed_red_pixels)
    
    # expand the bounding box to include the border
    min_row -=1
    min_col -=1
    max_row += 1
    max_col += 1
    
    # 3. Add new rows above and below
    output_grid = np.insert(output_grid, min_row, values=azure_color, axis=0)
    output_grid = np.insert(output_grid, max_row + 2, values=azure_color, axis=0)

    # Update the bounding box
    min_row_new = min_row
    max_row_new = max_row + 2 # add the two rows

    # 4. Fill expanded area with red
    for r in range(min_row_new, max_row_new + 1):
        for c in range(min_col, max_col + 1):
            if not (output_grid[r,c] == azure_color):
                output_grid[r, c] = red_color
                
    # 5. Add red corners
    if min_row_new > 0 and min_col > 0:
        output_grid[min_row_new-1, min_col-1] = red_color
    if min_row_new > 0 and max_col+1 < output_grid.shape[1]:
        output_grid[min_row_new-1, max_col+1] = red_color
    if max_row_new+1 < output_grid.shape[0] and min_col > 0:
        output_grid[max_row_new+1, min_col-1] = red_color
    if max_row_new+1 < output_grid.shape[0] and max_col+1 < output_grid.shape[1]:
        output_grid[max_row_new+1, max_col+1] = red_color

    return output_grid
```
