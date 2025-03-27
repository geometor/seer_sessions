```python
"""
1.  **Object Definition:** An object is a group of one or more diagonally or orthogonally connected pixels of the same color. The background is color 8.

2.  **Horizontal Extension:** For each row and each object within that row, if the object has a horizontal span greater than one, extend the object's color horizontally to any *directly adjacent* background (color 8) pixels *to the immediate left or right*. This extension happens only *one pixel* at a time.

3.  **Conditional Object Disappearance:**
    *   Iterate through each row from top to bottom (except the last row).
    *   For each multi-pixel horizontal object (span > 1) in the current row (N):
        *   Check if an object of the *same color* and *same horizontal span* exists directly below it on row (N+1).
        *   If no such object exists on row (N+1), then on row (N+1), create a new object of color 8 (background) with the *same horizontal span and x-coordinates* as the object from row N.

4.  **Last Row Rule:** For each pixel in the last row:
    *   If the pixel's color matches the color of *any* multi-pixel horizontal object (span > 1) found *anywhere* in the input grid, change the pixel's color to 8 (background). Otherwise, keep the original color.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid, including diagonals."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, color, obj)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited and grid[row, col] != 8:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))
    return objects

def get_horizontal_span(obj_pixels, row):
    """Calculates the horizontal span of an object on a specific row."""
    row_pixels = [c for r, c in obj_pixels if r == row]
    if not row_pixels:
        return 0, 0, 0  # No pixels on this row
    min_col = min(row_pixels)
    max_col = max(row_pixels)
    return min_col, max_col, max_col - min_col + 1

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    objects = find_objects(input_grid)

    # Horizontal Extension (One Pixel at a Time)
    for r in range(rows):
        for color, obj_pixels in objects:
            min_col, max_col, span = get_horizontal_span(obj_pixels, r)
            if span > 1:
                # Check left
                if min_col > 0 and output_grid[r, min_col - 1] == 8:
                    output_grid[r, min_col - 1] = color
                # Check right
                if max_col < cols - 1 and output_grid[r, max_col + 1] == 8:
                    output_grid[r, max_col + 1] = color
    
    objects = find_objects(output_grid) #need to recalculate the objects

    # Conditional Object Disappearance
    for r in range(rows - 1):
        for color, obj_pixels in objects:
            min_col, max_col, span = get_horizontal_span(obj_pixels, r)
            if span > 1:
                # Check for same color and span on next row
                next_row_min, next_row_max, next_row_span = get_horizontal_span(obj_pixels, r + 1)
                if not (next_row_span == span and any(c == color for c, _ in objects if get_horizontal_span(_, r+1)[2] == span)):
                    # Fill next row with 8 based on current row's span
                    for c in range(min_col, max_col + 1):
                        output_grid[r + 1, c] = 8

    # Last Row Rule
    for c in range(cols):
        color = output_grid[rows - 1, c]
        for other_color, other_obj_pixels in objects:
            if other_color == color:
                for rr in range(rows -1):
                  _,_, other_span = get_horizontal_span(other_obj_pixels, rr)
                  if other_span > 1:
                    output_grid[rows - 1, c] = 8
                    break # inner loop
            if output_grid[rows - 1, c] == 8:
              break; #outer loop

    return output_grid.tolist()
```