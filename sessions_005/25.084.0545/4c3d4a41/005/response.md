```python
"""
1.  **Identify Boundaries:**
    *   Find the top horizontal gray (5) line. This is the top boundary.
    *   For each column, find the highest row containing a gray (5) pixel *below* the top boundary. This defines the bottom boundary for that column.

2.  **Identify Objects:**
    *   Within the boundaries (between the top row and the column-specific bottom row), identify contiguous groups of pixels of the same color (excluding white/0 and gray/5). Each group is an object.

3.  **Shift Objects Left:**
    *   Iterate through each row within the boundaries.
    *   For each row:
        *   Find all objects present in that row.
        *   Shift each object in that row to the leftmost available position, respecting both gray boundaries and the positions of other objects already placed in that row.

"""

import numpy as np

def find_top_boundary(grid):
    """Finds the row index of the top horizontal gray line."""
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return i
    return -1

def find_bottom_boundaries(grid, top_row):
    """Finds the bottom boundary row for each column."""
    rows, cols = grid.shape
    bottom_boundaries = [-1] * cols

    for c in range(cols):
        for r in range(rows - 1, top_row, -1):
            if grid[r, c] == 5:
                bottom_boundaries[c] = r
                break  # Move to the next column
            elif r == top_row + 1:
                bottom_boundaries[c] = top_row # default if no grey
    return bottom_boundaries

def find_objects_in_row(grid, row, top_boundary, bottom_boundaries):
    """Finds objects within a specific row and given boundaries."""
    objects = []
    cols = grid.shape[1]
    visited = set()

    for c in range(cols):
        if (row, c) not in visited and grid[row, c] != 0 and grid[row, c] != 5:
            # boundary check
            if row > top_boundary and row <= bottom_boundaries[c]:
                object_pixels = []
                stack = [(row, c)]
                color = grid[row, c]

                while stack:
                    curr_r, curr_c = stack.pop()
                    if (curr_r, curr_c) in visited:
                        continue
                    visited.add((curr_r, curr_c))

                    if curr_r > top_boundary and curr_r <= bottom_boundaries[curr_c] and grid[curr_r, curr_c] == color:
                        object_pixels.append((curr_r, curr_c))
                        # Check only left and right neighbors since we're in the same row
                        for dc in [-1, 1]:
                            nc = curr_c + dc
                            if 0 <= nc < cols:
                                stack.append((curr_r, nc))
                if object_pixels:
                    objects.append({'color': color, 'pixels': object_pixels})

    return objects



def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Boundaries
    top_boundary = find_top_boundary(input_grid)
    bottom_boundaries = find_bottom_boundaries(input_grid, top_boundary)
    # 2. Iterate by row and shift within each row

    for r in range(rows):
      # Find objects
      objects = find_objects_in_row(input_grid, r, top_boundary, bottom_boundaries)

      # Clear original position
      for obj in objects:
        for _,c in obj['pixels']:
          output_grid[r,c] = 0

      # move to left-most
      for obj in objects:
          # sort by col to process left to right
          obj['pixels'].sort(key=lambda x:x[1])
          
          for _, orig_c in obj['pixels']:
              # Find leftmost available position in the row
              target_c = orig_c

              while target_c > 0:
                  if input_grid[r, target_c - 1] == 5 or (r > top_boundary and r <= bottom_boundaries[target_c] and output_grid[r, target_c - 1] == 0 ) :
                      target_c -= 1
                  else:
                      break
              output_grid[r, target_c] = obj['color']


    return output_grid
```