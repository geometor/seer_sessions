# d4f3cd78 • 002 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the Grey Shape:** Find the contiguous region(s) of grey (5) pixels in the input grid. This grey region appears designed to create a boundary, potentially fully enclosing an internal area, or presents some other specific, identifiable shape.

2.  **Determine the Interior:** Based on the identified grey shape, identify the region that it encloses or the inside of the shape.

3.  **Fill the Interior:** Change the color of all pixels within the determined "interior" region to azure (8).

4.  **Add Extra Azure:** From the now azure filled interior, in a consistent manner based on the original shape and its filled form, add extra azure (8) pixels. In the examples shown, this seems to occur by extending from the bottom of the filled shape. In the first case, a vertical line 2 blocks down from the lowest and furthest-right azure-colored pixel of the filled square. In the second example, there is an azure pixel added at the top of the upper horizontal line of the '5' shape, in the middle.
"""

import numpy as np

def find_grey_shape(grid):
    # Find coordinates of all grey (5) pixels.
    grey_pixels = np.argwhere(grid == 5)
    return grey_pixels

def flood_fill(grid, start_row, start_col, fill_color):
    """Performs a flood fill operation, starting from a given point."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    queue = [(start_row, start_col)]
    original_color = grid[start_row, start_col]

    if original_color == fill_color:
        return

    while queue:
        row, col = queue.pop(0)
        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue
        if visited[row, col] or grid[row, col] != original_color:
            continue

        grid[row, col] = fill_color
        visited[row, col] = True

        queue.append((row + 1, col))
        queue.append((row - 1, col))
        queue.append((row, col + 1))
        queue.append((row, col - 1))
        

def determine_interior(grid, grey_pixels):
    # Find a point inside
    if len(grey_pixels) == 0:
        return []
    
    min_row = np.min(grey_pixels[:, 0])
    max_row = np.max(grey_pixels[:, 0])
    min_col = np.min(grey_pixels[:, 1])
    max_col = np.max(grey_pixels[:, 1])
    
    for r in range(min_row + 1, max_row):
        for c in range(min_col+1, max_col):
            if grid[r,c] != 5:
                return (r,c)
    return None
    

def add_extra_azure(grid, grey_pixels, filled_coords):
    """Adds extra azure pixels based on the shape."""
    rows, cols = grid.shape

    if not filled_coords:
          # if the grey shape is open, pick point on grey shape to extend azure
          min_row = np.min(grey_pixels[:, 0])
          max_row = np.max(grey_pixels[:, 0])
          min_col = np.min(grey_pixels[:, 1])
          max_col = np.max(grey_pixels[:, 1])
          
          # Calculate the center of the bounding box
          center_row = (min_row + max_row) // 2
          center_col = (min_col + max_col) // 2
          
          if grid[min_row, center_col] == 5:
            # if the center top edge is grey, check above, fill
            if 0 <= min_row -1 and grid[min_row -1, center_col] == 0:
              for r in range(min_row -1, -1, -1):
                if 0<= r < rows:
                  grid[r,center_col] = 8

    else:  # fully enclosed
          # find the lowest right-most azure, and extend down
        lowest_row = -1
        rightmost_col = -1

        for row, col in filled_coords:
            if row > lowest_row:
              lowest_row = row
              rightmost_col = col
            elif row == lowest_row and col > rightmost_col:
              rightmost_col = col

        if 0 <= lowest_row + 1 < rows:
          grid[lowest_row+1, rightmost_col] = 8
        if 0 <= lowest_row + 2 < rows:
          grid[lowest_row+2, rightmost_col] = 8

    return


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)

    # 1. Identify the Grey Shape
    grey_pixels = find_grey_shape(output_grid)

    # 2. Determine the Interior
    interior_start = determine_interior(output_grid, grey_pixels)

    # 3. Fill the Interior
    filled_coords = []

    if interior_start:
        row, col = interior_start
        if output_grid[row,col] != 5:
            flood_fill(output_grid, row, col, 8)
            filled_coords = np.argwhere(output_grid == 8)

    # 4. Add Extra Azure
    add_extra_azure(output_grid, grey_pixels, filled_coords)

    return output_grid
```
