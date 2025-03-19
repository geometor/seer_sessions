# bc1d5164 • 008 • refine_coder

---
```python
"""
Identify the smallest closed shape in the input grid and extract it.  A closed
shape is defined as a contiguous region of non-black pixels where no pixel in
the region has a neighbor of the same color in any of the four cardinal
directions (up, down, left, right).
"""

import numpy as np

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def is_cardinally_connected(grid, r, c, color):
    """Checks if a pixel is cardinally connected to another pixel of the same color."""
    rows, cols = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
            return True
    return False

def find_connected_component(grid, start_r, start_c, color, visited):
    """
    Finds all pixels connected to the starting pixel using 8-connectivity.

    Args:
       grid: The numpy array representing the grid.
       start_r: Starting row.
       start_c: Starting column.
       color: Color of the connected component to search
       visited: A set of already visited pixel.

    Returns:
      A list of (row, col) tuples representing the connected component.
    """

    rows, cols = grid.shape
    component = []
    stack = [(start_r, start_c)]

    while stack:
        r, c = stack.pop()
        if (r,c) in visited:
            continue
        visited.add((r,c))

        if grid[r, c] == color:
          component.append((r, c))
          # Explore all 8 neighbors (including diagonals)
          for dr in [-1, 0, 1]:
              for dc in [-1, 0, 1]:
                  if dr == 0 and dc == 0:
                      continue
                  nr, nc = r + dr, c + dc
                  if 0 <= nr < rows and 0 <= nc < cols:
                      stack.append((nr, nc))
    return component

def find_closed_shapes(grid):
    """
    Find all closed shapes using flood fill and considering neighbors.

    Returns a list of sets, with a set per shape containing pixel coords (r,c)
    """
    rows, cols = grid.shape
    visited = set()
    closed_shapes = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r,c) not in visited:
                color = grid[r,c]
                component = find_connected_component(grid, r, c, color, visited)

                is_closed = True
                for pixel_r, pixel_c in component:
                    if is_cardinally_connected(grid, pixel_r, pixel_c, color):
                        is_closed = False
                        break

                if is_closed:
                    closed_shapes.append(set(component))
    return closed_shapes

def transform(input_grid):
    """
    Transforms the input grid by extracting the bounding box containing the
    smallest closed shape.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Find closed shapes
    closed_shapes = find_closed_shapes(input_array)

    # Find the smallest shape
    if not closed_shapes:
        return input_grid # Handle cases with no closed shapes
    smallest_shape = min(closed_shapes, key=len)

    # Find the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(smallest_shape)

    # Extract the subgrid
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```
