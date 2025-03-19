# 941d9a10 • 002 • example_3 • investigate_coder

---
```python
"""
The program identifies the patterned grey background structure, determines three key locations (top-left, center, bottom-right), and paints specific cells adjacent to these points with blue, red and green colors, respectively.
"""

import numpy as np

def find_grey_intersections(grid):
    """Finds intersection points of grey (5) lines."""
    intersections = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 5:
                # Check for horizontal and vertical grey lines
                if (c > 0 and grid[r, c-1] == 5) or (c < cols - 1 and grid[r, c+1] == 5):
                    if (r > 0 and grid[r-1, c] == 5) or (r < rows - 1 and grid[r+1, c] == 5):
                        intersections.append((r, c))
    return intersections

def get_top_left_intersection(intersections):
    """Returns the top-left intersection point."""
    if not intersections:
        return None
    return min(intersections, key=lambda p: (p[0], p[1]))

def get_bottom_right_intersection(intersections):
   """Returns the bottom-right intersection"""
   if not intersections:
      return None
   return max(intersections, key=lambda p:(p[0], p[1]))

def get_center_intersection(intersections, grid):
    """Finds a central intersection point."""
    #considers grey lines extending, not a single point
    if not intersections:
        return None

    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2

    closest_intersection = None
    min_dist = float('inf')

    for r, c in intersections:
        dist = abs(r - center_row) + abs(c - center_col)
        if dist < min_dist:
            min_dist = dist
            closest_intersection = (r,c)

    return closest_intersection


def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # find grey intersections
    intersections = find_grey_intersections(input_grid)

    # get insertion points
    top_left = get_top_left_intersection(intersections)
    bottom_right = get_bottom_right_intersection(intersections)
    center = get_center_intersection(intersections, input_grid)

   # Apply transformations
    if top_left:
      # find extend of grey, replace adjacent whites
        for r in range(top_left[0]):
            if output_grid[r,top_left[1]] == 0:
                output_grid[r, :top_left[1]] = 1


    if center:
        center_row, center_col = center
        # Paint red around the center intersection.  Find width of grey
        grey_width = 0
        for c in range(center_col,cols):
            if output_grid[center_row,c] == 5:
                grey_width +=1
            else:
                break

        start_col = center_col + grey_width
        if start_col < cols -1:
          output_grid[center_row-1:center_row+1, start_col:start_col+grey_width] = 2


    if bottom_right:
        grey_height = 0
        for r in range(bottom_right[0], rows):
            if output_grid[r, bottom_right[1]] == 5:
             grey_height += 1
            else:
                break
        if bottom_right[0] + grey_height < rows:
           output_grid[bottom_right[0] + grey_height:, bottom_right[1]:] = 3

    return output_grid
```
